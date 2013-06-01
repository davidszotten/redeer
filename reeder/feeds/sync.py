import time
import logging

from django.db import transaction
import eventlet

from reeder.feeds.models import Feed, Item


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


# def sync_feed(feed):
    # feedparser = eventlet.import_patched('feedparser')
    # pool = eventlet.GreenPool()

    # data = feedparser.parse(feed.url)
    # for entry in data['entries']:
        # sync_entry(feed, entry)
        # feed.set_last_updated()

feedparser = eventlet.import_patched('feedparser')
import q

def fetch_feed(feed, queue):
    q.q("fetching", feed)
    data = feedparser.parse(feed.url)
    q.q("done fetching", feed)
    # return feed, data
    queue.put((feed, data))


@transaction.commit_on_success
def sync_all():
    q.q("starting")
    # for feed in Feed.objects.all():
        # sync_feed(feed)
    feeds = Feed.objects.all()
    pool = eventlet.GreenPool()
    queue = eventlet.Queue()

    [pool.spawn_n(fetch_feed, feed, queue) for feed in feeds]

    # import feedparser
    # q.q("fetching feeds...")
    # feed_data = [feedparser.parse(feed.url) for feed in feeds]
    q.q("parsing feeds...")
    # for feed, data in zip(feeds, feed_data):
    # for feed, data in pool.imap(fetch_feed, feeds):
    q.q(pool.running(), queue.empty())
    while pool.running() or not queue.empty():
        feed, data = queue.get()

        q.q("parsing", feed)
        for entry in data['entries']:
            sync_entry(feed, entry)
            feed.set_last_updated()
        if pool.running():
            eventlet.sleep(.1)

    q.q("done")
