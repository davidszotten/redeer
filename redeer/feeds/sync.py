import time
import logging

from django.db import transaction
import eventlet
feedparser = eventlet.import_patched('feedparser')

from redeer.feeds.models import Feed, Item


_logger = logging.getLogger(__name__)


def sync_entry(feed, entry):
    try:
        url = entry['link']
        try:
            item = Item.objects.get(feed_id=feed.pk, url=url)
        except Item.DoesNotExist:
            item = Item(feed_id=feed.pk, url=url)

        item.title = entry['title']

        author = entry.get('author')
        if author is None:
            author = feed.title
        item.author = author

        item.html = entry['summary']

        published = entry.get('published_parsed')
        if published is None:
            published = entry.get('updated_parsed')

        item.created_on_time = int(time.mktime(published))
        item.save()
    except Exception as ex:
        _logger.error("Failed to sync entry {} for feed {}: {}".format(
            entry, feed, ex))


def fetch_feed(feed, queue):
    data = feedparser.parse(feed.url)
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
            feed.set_last_updated()
        if pool.running():
            eventlet.sleep(.1)
