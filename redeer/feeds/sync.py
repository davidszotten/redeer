import datetime
import time
import logging

from django.db import transaction
import eventlet
feedparser = eventlet.import_patched('feedparser')

from redeer.feeds.models import Feed, Item


_logger = logging.getLogger(__name__)


def to_epoch(parsed_time):
    return int(time.mktime(parsed_time))


def sync_entry(feed, entry):
    try:
        url = entry['link']
        id_ = entry.get('id', url)
        try:
            item = Item.objects.get(feed_id=feed.pk, url=url)
        except Item.DoesNotExist:
            item = Item(feed_id=feed.pk, url=url)

        item.item_id = id_
        item.title = entry['title']

        author = entry.get('author')
        if author is None:
            author = feed.title
        item.author = author

        item.html = entry['summary']

        published = entry.get('published_parsed')
        if published is None:
            published = entry.get('updated_parsed')

        item.created_on_time = to_epoch(published)
        item.save()
    except Exception as ex:
        _logger.error("Failed to sync entry {} for feed {}: {}".format(
            entry, feed, ex))


def fetch_feed(feed, queue):
    if feed.last_updated:
        modified_at = datetime.datetime.fromtimestamp(feed.last_updated)
    else:
        modified_at = None
    data = feedparser.parse(feed.url, modified=modified_at)
    queue.put((feed, data))


@transaction.commit_on_success
def sync_all():
    feeds = Feed.objects.all()
    pool = eventlet.GreenPool()
    queue = eventlet.Queue()

    [pool.spawn_n(fetch_feed, feed, queue) for feed in feeds]

    while pool.running() or not queue.empty():
        feed, data = queue.get()

        for entry in data['entries']:
            sync_entry(feed, entry)

        modified_parsed = data.get('modified_parsed')
        if isinstance(modified_parsed, time.struct_time):
            modified_at = to_epoch(modified_parsed)
        else:
            modified_at = None
        feed.set_last_updated(modified_at)

        if pool.running():
            eventlet.sleep(.1)
