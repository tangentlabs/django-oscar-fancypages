# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('assets', '0001_initial'),
        ('catalogue', '0009_auto__add_field_product_rating'),
        ('promotions', '0001_initial'),
        ('offer', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'FancyPage'
        db.create_table('fancypages_fancypage', (
            ('category_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.Category'], unique=True, primary_key=True)),
            ('page_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pages', null=True, to=orm['fancypages.PageType'])),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=15)),
            ('date_visible_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_visible_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('fancypages', ['FancyPage'])

        # Adding M2M table for field visibility_types on 'FancyPage'
        db.create_table('fancypages_fancypage_visibility_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fancypage', models.ForeignKey(orm['fancypages.fancypage'], null=False)),
            ('visibilitytype', models.ForeignKey(orm['fancypages.visibilitytype'], null=False))
        ))
        db.create_unique('fancypages_fancypage_visibility_types', ['fancypage_id', 'visibilitytype_id'])

        # Adding model 'PageType'
        db.create_table('fancypages_pagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('fancypages', ['PageType'])

        # Adding model 'VisibilityType'
        db.create_table('fancypages_visibilitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('fancypages', ['VisibilityType'])

        # Adding model 'Container'
        db.create_table('fancypages_container', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('fancypages', ['Container'])

        # Adding unique constraint on 'Container', fields ['name', 'content_type', 'object_id']
        db.create_unique('fancypages_container', ['name', 'content_type_id', 'object_id'])

        # Adding model 'OrderedContainer'
        db.create_table('fancypages_orderedcontainer', (
            ('container_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.Container'], unique=True, primary_key=True)),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('fancypages', ['OrderedContainer'])

        # Adding model 'ContentBlock'
        db.create_table('fancypages_contentblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blocks', to=orm['fancypages.Container'])),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('fancypages', ['ContentBlock'])

        # Adding model 'TextBlock'
        db.create_table('fancypages_textblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default='Your text goes here.')),
        ))
        db.send_create_signal('fancypages', ['TextBlock'])

        # Adding model 'TitleTextBlock'
        db.create_table('fancypages_titletextblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Your title goes here.', max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(default='Your text goes here.')),
        ))
        db.send_create_signal('fancypages', ['TitleTextBlock'])

        # Adding model 'ImageBlock'
        db.create_table('fancypages_imageblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('alt_text', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_asset', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='image_blocks', null=True, to=orm['assets.ImageAsset'])),
        ))
        db.send_create_signal('fancypages', ['ImageBlock'])

        # Adding model 'ImageAndTextBlock'
        db.create_table('fancypages_imageandtextblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('alt_text', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_asset', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='image_text_blocks', null=True, to=orm['assets.ImageAsset'])),
            ('text', self.gf('django.db.models.fields.CharField')(default='Your text goes here.', max_length=2000)),
        ))
        db.send_create_signal('fancypages', ['ImageAndTextBlock'])

        # Adding model 'CarouselBlock'
        db.create_table('fancypages_carouselblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('image_1', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_1', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_2', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_2', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_3', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_3', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_4', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_4', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_5', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_5', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_6', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_6', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_7', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_7', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_8', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_8', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_9', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_9', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image_10', self.gf('fancypages.assets.fields.AssetKey')(blank=True, related_name='+', null=True, to=orm['assets.ImageAsset'])),
            ('link_url_10', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('fancypages', ['CarouselBlock'])

        # Adding model 'PageNavigationBlock'
        db.create_table('fancypages_pagenavigationblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('fancypages', ['PageNavigationBlock'])

        # Adding model 'PrimaryNavigationBlock'
        db.create_table('fancypages_primarynavigationblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('fancypages', ['PrimaryNavigationBlock'])

        # Adding model 'TabBlock'
        db.create_table('fancypages_tabblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('fancypages', ['TabBlock'])

        # Adding model 'TwoColumnLayoutBlock'
        db.create_table('fancypages_twocolumnlayoutblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('left_width', self.gf('django.db.models.fields.PositiveIntegerField')(default=6, max_length=3)),
        ))
        db.send_create_signal('fancypages', ['TwoColumnLayoutBlock'])

        # Adding model 'ThreeColumnLayoutBlock'
        db.create_table('fancypages_threecolumnlayoutblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('fancypages', ['ThreeColumnLayoutBlock'])

        # Adding model 'FourColumnLayoutBlock'
        db.create_table('fancypages_fourcolumnlayoutblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('fancypages', ['FourColumnLayoutBlock'])

        # Adding model 'VideoBlock'
        db.create_table('fancypages_videoblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('video_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('fancypages', ['VideoBlock'])

        # Adding model 'TwitterBlock'
        db.create_table('fancypages_twitterblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('max_tweets', self.gf('django.db.models.fields.PositiveIntegerField')(default=5)),
        ))
        db.send_create_signal('fancypages', ['TwitterBlock'])

        # Adding model 'SingleProductBlock'
        db.create_table('fancypages_singleproductblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'], null=True)),
        ))
        db.send_create_signal('fancypages', ['SingleProductBlock'])

        # Adding model 'HandPickedProductsPromotionBlock'
        db.create_table('fancypages_handpickedproductspromotionblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('promotion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotions.HandPickedProductList'], null=True)),
        ))
        db.send_create_signal('fancypages', ['HandPickedProductsPromotionBlock'])

        # Adding model 'AutomaticProductsPromotionBlock'
        db.create_table('fancypages_automaticproductspromotionblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('promotion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotions.AutomaticProductList'], null=True)),
        ))
        db.send_create_signal('fancypages', ['AutomaticProductsPromotionBlock'])

        # Adding model 'OfferBlock'
        db.create_table('fancypages_offerblock', (
            ('contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['offer.ConditionalOffer'], null=True)),
        ))
        db.send_create_signal('fancypages', ['OfferBlock'])


    def backwards(self, orm):
        # Removing unique constraint on 'Container', fields ['name', 'content_type', 'object_id']
        db.delete_unique('fancypages_container', ['name', 'content_type_id', 'object_id'])

        # Deleting model 'FancyPage'
        db.delete_table('fancypages_fancypage')

        # Removing M2M table for field visibility_types on 'FancyPage'
        db.delete_table('fancypages_fancypage_visibility_types')

        # Deleting model 'PageType'
        db.delete_table('fancypages_pagetype')

        # Deleting model 'VisibilityType'
        db.delete_table('fancypages_visibilitytype')

        # Deleting model 'Container'
        db.delete_table('fancypages_container')

        # Deleting model 'OrderedContainer'
        db.delete_table('fancypages_orderedcontainer')

        # Deleting model 'ContentBlock'
        db.delete_table('fancypages_contentblock')

        # Deleting model 'TextBlock'
        db.delete_table('fancypages_textblock')

        # Deleting model 'TitleTextBlock'
        db.delete_table('fancypages_titletextblock')

        # Deleting model 'ImageBlock'
        db.delete_table('fancypages_imageblock')

        # Deleting model 'ImageAndTextBlock'
        db.delete_table('fancypages_imageandtextblock')

        # Deleting model 'CarouselBlock'
        db.delete_table('fancypages_carouselblock')

        # Deleting model 'PageNavigationBlock'
        db.delete_table('fancypages_pagenavigationblock')

        # Deleting model 'PrimaryNavigationBlock'
        db.delete_table('fancypages_primarynavigationblock')

        # Deleting model 'TabBlock'
        db.delete_table('fancypages_tabblock')

        # Deleting model 'TwoColumnLayoutBlock'
        db.delete_table('fancypages_twocolumnlayoutblock')

        # Deleting model 'ThreeColumnLayoutBlock'
        db.delete_table('fancypages_threecolumnlayoutblock')

        # Deleting model 'FourColumnLayoutBlock'
        db.delete_table('fancypages_fourcolumnlayoutblock')

        # Deleting model 'VideoBlock'
        db.delete_table('fancypages_videoblock')

        # Deleting model 'TwitterBlock'
        db.delete_table('fancypages_twitterblock')

        # Deleting model 'SingleProductBlock'
        db.delete_table('fancypages_singleproductblock')

        # Deleting model 'HandPickedProductsPromotionBlock'
        db.delete_table('fancypages_handpickedproductspromotionblock')

        # Deleting model 'AutomaticProductsPromotionBlock'
        db.delete_table('fancypages_automaticproductspromotionblock')

        # Deleting model 'OfferBlock'
        db.delete_table('fancypages_offerblock')


    models = {
        'assets.imageasset': {
            'Meta': {'object_name': 'ImageAsset'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'catalogue.attributeentity': {
            'Meta': {'object_name': 'AttributeEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': "orm['catalogue.AttributeEntityType']"})
        },
        'catalogue.attributeentitytype': {
            'Meta': {'object_name': 'AttributeEntityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        'catalogue.attributeoption': {
            'Meta': {'object_name': 'AttributeOption'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['catalogue.AttributeOptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalogue.attributeoptiongroup': {
            'Meta': {'object_name': 'AttributeOptionGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'catalogue.category': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Category'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'catalogue.option': {
            'Meta': {'object_name': 'Option'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Required'", 'max_length': '128'})
        },
        'catalogue.product': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Product'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.ProductAttribute']", 'through': "orm['catalogue.ProductAttributeValue']", 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Category']", 'through': "orm['catalogue.ProductCategory']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_discountable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': "orm['catalogue.Product']"}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.ProductClass']", 'null': 'True'}),
            'product_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'recommended_products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Product']", 'symmetrical': 'False', 'through': "orm['catalogue.ProductRecommendation']", 'blank': 'True'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'relations'", 'blank': 'True', 'to': "orm['catalogue.Product']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.productattribute': {
            'Meta': {'ordering': "['code']", 'object_name': 'ProductAttribute'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AttributeEntityType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AttributeOptionGroup']", 'null': 'True', 'blank': 'True'}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'attributes'", 'null': 'True', 'to': "orm['catalogue.ProductClass']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'})
        },
        'catalogue.productattributevalue': {
            'Meta': {'object_name': 'ProductAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.ProductAttribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute_values'", 'to': "orm['catalogue.Product']"}),
            'value_boolean': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AttributeEntity']", 'null': 'True', 'blank': 'True'}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_integer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AttributeOption']", 'null': 'True', 'blank': 'True'}),
            'value_richtext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.productcategory': {
            'Meta': {'ordering': "['-is_canonical']", 'object_name': 'ProductCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_canonical': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Product']"})
        },
        'catalogue.productclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProductClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'track_stock': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'catalogue.productrecommendation': {
            'Meta': {'object_name': 'ProductRecommendation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_recommendations'", 'to': "orm['catalogue.Product']"}),
            'ranking': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Product']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fancypages.automaticproductspromotionblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'AutomaticProductsPromotionBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.AutomaticProductList']", 'null': 'True'})
        },
        'fancypages.carouselblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'CarouselBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_1': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_10': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_2': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_3': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_4': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_5': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_6': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_7': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_8': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_9': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link_url_1': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_10': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_2': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_3': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_4': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_5': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_6': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_7': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_8': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_9': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.container': {
            'Meta': {'unique_together': "(('name', 'content_type', 'object_id'),)", 'object_name': 'Container'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'fancypages.contentblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'ContentBlock'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocks'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fancypages.fancypage': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'FancyPage', '_ormbases': ['catalogue.Category']},
            'category_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.Category']", 'unique': 'True', 'primary_key': 'True'}),
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['fancypages.PageType']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '15'}),
            'visibility_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fancypages.VisibilityType']", 'symmetrical': 'False'})
        },
        'fancypages.fourcolumnlayoutblock': {
            'Meta': {'object_name': 'FourColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.handpickedproductspromotionblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'HandPickedProductsPromotionBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.HandPickedProductList']", 'null': 'True'})
        },
        'fancypages.imageandtextblock': {
            'Meta': {'object_name': 'ImageAndTextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_text_blocks'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "'Your text goes here.'", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.imageblock': {
            'Meta': {'object_name': 'ImageBlock', '_ormbases': ['fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_blocks'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.offerblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'OfferBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.ConditionalOffer']", 'null': 'True'})
        },
        'fancypages.orderedcontainer': {
            'Meta': {'object_name': 'OrderedContainer', '_ormbases': ['fancypages.Container']},
            'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'fancypages.pagenavigationblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'PageNavigationBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fancypages.primarynavigationblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'PrimaryNavigationBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.singleproductblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'SingleProductBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Product']", 'null': 'True'})
        },
        'fancypages.tabblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TabBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.textblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"})
        },
        'fancypages.threecolumnlayoutblock': {
            'Meta': {'object_name': 'ThreeColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.titletextblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TitleTextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Your title goes here.'", 'max_length': '100'})
        },
        'fancypages.twitterblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TwitterBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'max_tweets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fancypages.twocolumnlayoutblock': {
            'Meta': {'object_name': 'TwoColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'left_width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6', 'max_length': '3'})
        },
        'fancypages.videoblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'VideoBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video_code': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fancypages.visibilitytype': {
            'Meta': {'object_name': 'VisibilityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'offer.benefit': {
            'Meta': {'object_name': 'Benefit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_affected_items': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'proxy_class': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.Range']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'value': ('oscar.models.fields.PositiveDecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        },
        'offer.condition': {
            'Meta': {'object_name': 'Condition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proxy_class': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.Range']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'value': ('oscar.models.fields.PositiveDecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        },
        'offer.conditionaloffer': {
            'Meta': {'ordering': "['-priority']", 'object_name': 'ConditionalOffer'},
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.Benefit']"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.Condition']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_basket_applications': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'max_global_applications': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_user_applications': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'num_applications': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_orders': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'offer_type': ('django.db.models.fields.CharField', [], {'default': "'Site'", 'max_length': '128'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'redirect_url': ('oscar.models.fields.ExtendedURLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'unique': 'True', 'null': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '64'}),
            'total_discount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        'offer.range': {
            'Meta': {'object_name': 'Range'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'classes'", 'blank': 'True', 'to': "orm['catalogue.ProductClass']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excluded_products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'excludes'", 'blank': 'True', 'to': "orm['catalogue.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'includes'", 'blank': 'True', 'to': "orm['catalogue.Category']"}),
            'included_products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'includes'", 'blank': 'True', 'to': "orm['catalogue.Product']"}),
            'includes_all_products': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'proxy_class': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'promotions.automaticproductlist': {
            'Meta': {'object_name': 'AutomaticProductList'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link_url': ('oscar.models.fields.ExtendedURLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_products': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'})
        },
        'promotions.handpickedproductlist': {
            'Meta': {'object_name': 'HandPickedProductList'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link_url': ('oscar.models.fields.ExtendedURLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalogue.Product']", 'null': 'True', 'through': "orm['promotions.OrderedProduct']", 'blank': 'True'})
        },
        'promotions.keywordpromotion': {
            'Meta': {'object_name': 'KeywordPromotion'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'filter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'promotions.orderedproduct': {
            'Meta': {'ordering': "('display_order',)", 'object_name': 'OrderedProduct'},
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.HandPickedProductList']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Product']"})
        },
        'promotions.pagepromotion': {
            'Meta': {'object_name': 'PagePromotion'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'page_url': ('oscar.models.fields.ExtendedURLField', [], {'max_length': '128', 'db_index': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fancypages']
