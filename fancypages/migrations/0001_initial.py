# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PageType'
        db.create_table('fancypages_pagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('fancypages', ['PageType'])

        # Adding model 'Page'
        db.create_table('fancypages_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('page_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['fancypages.PageType'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['fancypages.Page'])),
            ('relative_url', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=15)),
            ('date_visible_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_visible_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('fancypages', ['Page'])

        # Adding model 'Container'
        db.create_table('fancypages_container', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variable_name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='containers', to=orm['fancypages.Page'])),
        ))
        db.send_create_signal('fancypages', ['Container'])

        # Adding model 'TextWidget'
        db.create_table('fancypages_textwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='textwidgets', to=orm['fancypages.Container'])),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('fancypages', ['TextWidget'])

        # Adding model 'TitleTextWidget'
        db.create_table('fancypages_titletextwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titletextwidgets', to=orm['fancypages.Container'])),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('fancypages', ['TitleTextWidget'])

        # Adding model 'ImageWidget'
        db.create_table('fancypages_imagewidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagewidgets', to=orm['fancypages.Container'])),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('fancypages', ['ImageWidget'])


    def backwards(self, orm):
        
        # Deleting model 'PageType'
        db.delete_table('fancypages_pagetype')

        # Deleting model 'Page'
        db.delete_table('fancypages_page')

        # Deleting model 'Container'
        db.delete_table('fancypages_container')

        # Deleting model 'TextWidget'
        db.delete_table('fancypages_textwidget')

        # Deleting model 'TitleTextWidget'
        db.delete_table('fancypages_titletextwidget')

        # Deleting model 'ImageWidget'
        db.delete_table('fancypages_imagewidget')


    models = {
        'fancypages.container': {
            'Meta': {'object_name': 'Container'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'containers'", 'to': "orm['fancypages.Page']"}),
            'variable_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'fancypages.imagewidget': {
            'Meta': {'object_name': 'ImageWidget'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagewidgets'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'fancypages.page': {
            'Meta': {'object_name': 'Page'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['fancypages.PageType']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['fancypages.Page']"}),
            'relative_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'fancypages.textwidget': {
            'Meta': {'object_name': 'TextWidget'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'textwidgets'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'fancypages.titletextwidget': {
            'Meta': {'object_name': 'TitleTextWidget'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titletextwidgets'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fancypages']
