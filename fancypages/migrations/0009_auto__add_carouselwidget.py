# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CarouselWidget'
        db.create_table('fancypages_carouselwidget', (
            ('widget_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.Widget'], unique=True, primary_key=True)),
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
        db.send_create_signal('fancypages', ['CarouselWidget'])


    def backwards(self, orm):
        # Deleting model 'CarouselWidget'
        db.delete_table('fancypages_carouselwidget')


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
        'fancypages.automaticproductspromotionwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'AutomaticProductsPromotionWidget', '_ormbases': ['fancypages.Widget']},
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.AutomaticProductList']", 'null': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.carouselwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'CarouselWidget', '_ormbases': ['fancypages.Widget']},
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
            'link_url_9': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.container': {
            'Meta': {'unique_together': "(('variable_name', 'content_type', 'object_id'),)", 'object_name': 'Container'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'variable_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.fourcolumnlayoutwidget': {
            'Meta': {'object_name': 'FourColumnLayoutWidget'},
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.handpickedproductspromotionwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'HandPickedProductsPromotionWidget', '_ormbases': ['fancypages.Widget']},
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.HandPickedProductList']", 'null': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.imageandtextwidget': {
            'Meta': {'object_name': 'ImageAndTextWidget', '_ormbases': ['fancypages.Widget']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_text_widgets'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "'Your text goes here.'", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.imagewidget': {
            'Meta': {'object_name': 'ImageWidget', '_ormbases': ['fancypages.Widget']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_widgets'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.offerwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'OfferWidget', '_ormbases': ['fancypages.Widget']},
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.ConditionalOffer']", 'null': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.orderedcontainer': {
            'Meta': {'object_name': 'OrderedContainer', '_ormbases': ['fancypages.Container']},
            'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'fancypages.page': {
            'Meta': {'object_name': 'Page'},
            'category': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'page'", 'unique': 'True', 'to': "orm['catalogue.Category']"}),
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['fancypages.PageType']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '15'})
        },
        'fancypages.pagenavigationwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'PageNavigationWidget', '_ormbases': ['fancypages.Widget']},
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'template_name': ('django.db.models.fields.CharField', [], {'default': "'fancypages/pages/page.html'", 'max_length': '255'})
        },
        'fancypages.primarynavigationwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'PrimaryNavigationWidget', '_ormbases': ['fancypages.Widget']},
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.singleproductwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'SingleProductWidget', '_ormbases': ['fancypages.Widget']},
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Product']", 'null': 'True'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.tabwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TabWidget', '_ormbases': ['fancypages.Widget']},
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.textwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TextWidget', '_ormbases': ['fancypages.Widget']},
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.threecolumnlayoutwidget': {
            'Meta': {'object_name': 'ThreeColumnLayoutWidget'},
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.titletextwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TitleTextWidget', '_ormbases': ['fancypages.Widget']},
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Your title goes here.'", 'max_length': '100'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.twitterwidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TwitterWidget', '_ormbases': ['fancypages.Widget']},
            'max_tweets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.twocolumnlayoutwidget': {
            'Meta': {'object_name': 'TwoColumnLayoutWidget'},
            'left_width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6', 'max_length': '3'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.videowidget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'VideoWidget', '_ormbases': ['fancypages.Widget']},
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Widget']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.widget': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Widget'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widgets'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'offer.benefit': {
            'Meta': {'object_name': 'Benefit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_affected_items': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['offer.Range']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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