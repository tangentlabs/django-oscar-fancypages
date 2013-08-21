from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages.models import ContentBlock
from fancypages.library import register_content_block


Product = models.get_model('catalogue', 'Product')


@register_content_block
class SingleProductBlock(ContentBlock):
    name = _("Single Product")
    code = 'single-product'
    group = _("Catalogue")
    template_name = "fancypages/blocks/productblock.html"

    product = models.ForeignKey(
        'catalogue.Product',
        verbose_name=_("Single Product"), null=True, blank=False)

    def __unicode__(self):
        if self.product:
            return u"Product '%s'" % self.product.upc
        return u"Product '%s'" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class HandPickedProductsPromotionBlock(ContentBlock):
    name = _("Hand Picked Products Promotion")
    code = 'promotion-hand-picked-products'
    group = _("Catalogue")
    template_name = "fancypages/blocks/promotionblock.html"

    promotion = models.ForeignKey(
        'promotions.HandPickedProductList',
        verbose_name=_("Hand Picked Products Promotion"), null=True, blank=False)

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '%s'" % self.promotion.pk
        return u"Promotion '%s'" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class AutomaticProductsPromotionBlock(ContentBlock):
    name = _("Automatic Products Promotion")
    code = 'promotion-ordered-products'
    group = _("Catalogue")
    template_name = "fancypages/blocks/promotionblock.html"

    promotion = models.ForeignKey(
        'promotions.AutomaticProductList',
        verbose_name=_("Automatic Products Promotion"), null=True, blank=False)

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '%s'" % self.promotion.pk
        return u"Promotion '%s'" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class OfferBlock(ContentBlock):
    name = _("Offer Products")
    code = 'products-range'
    group = _("Catalogue")
    template_name = "fancypages/blocks/offerblock.html"

    offer = models.ForeignKey(
        'offer.ConditionalOffer',
        verbose_name=_("Offer"), null=True, blank=False)

    @property
    def products(self):
        range = self.offer.condition.range
        if range.includes_all_products:
            return Product.browsable.filter(is_discountable=True)
        return range.included_products.filter(is_discountable=True)

    def __unicode__(self):
        if self.offer:
            return u"Offer '%s'" % self.offer.pk
        return u"Offer '%s'" % self.id

    class Meta:
        app_label = 'fancypages'


@register_content_block
class PrimaryNavigationBlock(ContentBlock):
    name = _("Primary Navigation")
    code = 'primary-navigation'
    group = _("Content")
    template_name = "fancypages/blocks/primary_navigation_block.html"

    def __unicode__(self):
        return u'Primary Navigation'

    class Meta:
        app_label = 'fancypages'
