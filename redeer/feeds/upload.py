from xml.dom.minidom import parse

from redeer.feeds.models import Group, Feed


def import_google_reader(file_handle):
    parser = HandleGoogleReader(file_handle)
    for feed in parser.feeds.values():
        group, _ = Group.objects.get_or_create(title=feed['group'])
        Feed.objects.get_or_create(
            title=feed['title'],
            url=feed['xmlUrl'],
            website=feed['htmlUrl'],
            group = group
        )


class HandleGoogleReader(object):
    def __init__(self, file_handle):
        self.feeds = {}

        dom = parse(file_handle)
        body = dom.getElementsByTagName("body")[0]
        self.handle_body(body)

    def get_text(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def childOutlines(self, element):
        return [el for el in element.getElementsByTagName("outline")
            if el.parentNode is element]

    def handle_body(self, body):
        for group in self.childOutlines(body):
            self.handle_group(group)

    def handle_group(self, group):
        attributes = dict(group.attributes.items())
        title = attributes['title']
        for feed in self.childOutlines(group):
            self.handle_feed(feed, title)

    def handle_feed(self, feed, group_name):
        attributes = dict(feed.attributes.items())
        title = attributes['title']
        attributes['group'] = group_name
        assert title not in self.feeds
        self.feeds[title] = attributes
