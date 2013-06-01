from django.db import models


DEFAULT_MAX = 500


class Group(models.Model):
    title = models.CharField(max_length=DEFAULT_MAX)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
        }

    def feed_ids(self):
        return ','.join(map(str, self.feed_set.values_list('pk', flat=True)))

    def to_feedgroup_dict(self):
        return {
            'group_id': self.pk,
            'feed_ids': self.feed_ids(),
        }


class Feed(models.Model):
    title = models.CharField(max_length=DEFAULT_MAX)
    url = models.CharField(max_length=DEFAULT_MAX)
    website = models.CharField(max_length=DEFAULT_MAX)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            # 'favicon_id':
            'title': self.title,
            'url': self.url,
            'site_url': self.website,
            # 'is_spark':
            # 'last_updated_on_time':
        }
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
    author = models.CharField(max_length=DEFAULT_MAX)
    html = models.TextField()
    url = models.CharField(max_length=DEFAULT_MAX)
    is_saved = models.BooleanField()
    is_read = models.BooleanField()
    created_on_time = models.IntegerField()

    def __unicode__(self):
        return self.title
