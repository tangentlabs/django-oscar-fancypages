# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PageTemplate'
        db.create_table('fancypages_pagetemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('fancypages', ['PageTemplate'])

        # Adding model 'PageType'
        db.create_table('fancypages_pagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='page_types', to=orm['fancypages.PageTemplate'])),
        ))
        db.send_create_signal('fancypages', ['PageType'])

        # Adding model 'Page'
        db.create_table('fancypages_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('page_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['fancypages.PageType'])),
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

        # Adding model 'Widget'
        db.create_table('fancypages_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='widgets', to=orm['fancypages.Container'])),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('fancypages', ['Widget'])

        # Adding model 'TextWidget'
        db.create_table('fancypages_textwidget', (
            ('widget_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.Widget'], unique=True, primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(default='Your text goes here.', max_length=2000)),
        ))
        db.send_create_signal('fancypages', ['TextWidget'])

        # Adding model 'TitleTextWidget'
        db.create_table('fancypages_titletextwidget', (
            ('widget_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.Widget'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Your title goes here.', max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(default='Your text goes here.', max_length=2000)),
        ))
        db.send_create_signal('fancypages', ['TitleTextWidget'])

        # Adding model 'ImageWidget'
        db.create_table('fancypages_imagewidget', (
            ('widget_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.Widget'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('fancypages', ['ImageWidget'])


    def backwards(self, orm):
        
        # Deleting model 'PageTemplate'
        db.delete_table('fancypages_pagetemplate')

        # Deleting model 'PageType'
        db.delete_table('fancypages_pagetype')

        # Deleting model 'Page'
        db.delete_table('fancypages_page')

        # Deleting model 'Container'
        db.delete_table('fancypages_container')

        # Deleting model 'Widget'
        db.delete_table('fancypages_widget')

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
            'Meta': {'ordering': "['display_order']", 'object_name': 'ImageWidget', '_ormbases': ['fancypages.Widget']},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.page': {
            'Meta': {'object_name': 'Page'},
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['fancypages.PageType']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'relative_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fancypages.pagetemplate': {
            'Meta': {'object_name': 'PageTemplate'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_types'", 'to': "orm['fancypages.PageTemplate']"})
        },
        'fancypages.textwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TextWidget', '_ormbases': ['fancypages.Widget']},
            'text': ('django.db.models.fields.CharField', [], {'default': "'Your text goes here.'", 'max_length': '2000'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.titletextwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TitleTextWidget', '_ormbases': ['fancypages.Widget']},
            'text': ('django.db.models.fields.CharField', [], {'default': "'Your text goes here.'", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Your title goes here.'", 'max_length': '100'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.widget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Widget'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widgets'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fancypages']
