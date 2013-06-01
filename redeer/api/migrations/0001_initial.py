# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApiKey'
        db.create_table(u'api_apikey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'api', ['ApiKey'])


    def backwards(self, orm):
        # Deleting model 'ApiKey'
        db.delete_table(u'api_apikey')


    models = {
        u'api.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['api']