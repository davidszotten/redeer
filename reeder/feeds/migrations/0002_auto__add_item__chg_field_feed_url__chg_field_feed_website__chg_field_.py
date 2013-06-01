# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'feeds_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('is_saved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_on_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'feeds', ['Item'])


        # Changing field 'Feed.url'
        db.alter_column(u'feeds_feed', 'url', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Feed.website'
        db.alter_column(u'feeds_feed', 'website', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Feed.title'
        db.alter_column(u'feeds_feed', 'title', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'Group.title'
        db.alter_column(u'feeds_group', 'title', self.gf('django.db.models.fields.CharField')(max_length=500))

    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'feeds_item')


        # Changing field 'Feed.url'
        db.alter_column(u'feeds_feed', 'url', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Feed.website'
        db.alter_column(u'feeds_feed', 'website', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Feed.title'
        db.alter_column(u'feeds_feed', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Group.title'
        db.alter_column(u'feeds_group', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'feeds.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'feeds.item': {
            'Meta': {'object_name': 'Item'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'created_on_time': ('django.db.models.fields.IntegerField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Feed']"}),
            'html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['feeds']