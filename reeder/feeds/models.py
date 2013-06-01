import datetime

from django.db import models

from reeder.feeds.utils import to_timestamp


def to_comma_separated(lst):
    return ','.join(map(str, lst))


def mark_read(qs, is_read):
    qs.update(is_read=is_read)


class Group(models.Model):
    title = models.TextField()

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
        }

    def feed_ids(self):
        return to_comma_separated(self.feed_set.values_list('pk', flat=True))

    def to_feedgroup_dict(self):
        return {
            'group_id': self.pk,
            'feed_ids': self.feed_ids(),
        }

    def mark_read(self, is_read):
        mark_read(Item.objects.filter(feed_group__id=self.pk), is_read)


class Feed(models.Model):
    title = models.TextField()
    url = models.TextField()
    website = models.TextField()
    group = models.ForeignKey(Group)
    last_updated = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            # 'favicon_id':  reeder handles this by itself
            'title': self.title,
            'url': self.url,
            'site_url': self.website,
            # 'is_spark':
            'last_updated_on_time': self.last_updated,
        }

    def set_last_updated(self):
        self.last_updated = to_timestamp(datetime.datetime.now())
        self.save()

    def mark_read(self, is_read):
        mark_read(Item.objects.filter(feed_id=self.pk), is_read)

"""
id (positive integer)
favicon_id (positive integer)
title (utf-8 string)
url (utf-8 string)
site_url (utf-8 string)
is_spark (boolean integer)
last_updated_on_time (Unix timestamp/integer)
"""


class Item(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.TextField()
    author = models.TextField()
    html = models.TextField()
    url = models.TextField()
    is_saved = models.BooleanField()
    is_read = models.BooleanField()
    created_on_time = models.IntegerField()

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'feed_id': self.feed_id,
            'title': self.title,
            'author': self.author,
            'html': self.html,
            'url': self.url,
            'is_saved': int(self.is_saved),
            'is_read': int(self.is_read),
            'created_on_time': self.created_on_time,
    }

    def mark_read(self, is_read):
        mark_read(Item.objects.filter(pk=self.pk), is_read)

"""
id (positive integer)
feed_id (positive integer)
title (utf-8 string)
author (utf-8 string)
html (utf-8 string)
url (utf-8 string)
is_saved (boolean integer)
is_read (boolean integer)
created_on_time (Unix timestamp/integer)
"""
