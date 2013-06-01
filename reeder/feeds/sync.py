import time
import logging

from feedparser import parse

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


def sync_feed(feed):
    data = parse(feed.url)
    for entry in data['entries']:
        sync_entry(feed, entry)
        feed.set_last_updated()


def sync_all():
    for feed in Feed.objects.all():
        sync_feed(feed)
