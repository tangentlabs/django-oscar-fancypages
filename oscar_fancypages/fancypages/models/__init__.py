from __future__ import absolute_import

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from fancypages import manager
from fancypages import abstract_models

Category = models.get_model('catalogue', 'Category')


class FancyPage(Category, abstract_models.AbstractFancyPage):
    objects = manager.PageManager()

    @models.permalink
    def get_absolute_url(self):
        # make sure that the home view is actually redirecting to '/'
        # and not to '/home/'.
        if self.slug == slugify(getattr(settings, 'FP_HOMEPAGE_NAME')):
            return ('home', (), {})
        return ('fancypages:page-detail', (), {'slug': self.slug})


# We have to import all models from django-fancypages AFTER re-defining
# FancyPage because otherwise we'll import it FancyPage first and will use
# the wrong one.
from fancypages.models import (
    FancyPage,
    VisibilityType,
    PageType,
    Container,
    OrderedContainer,
    ImageMetadataMixin,
    NamedLinkMixin,
    TabBlock,
    TwoColumnLayoutBlock,
    ThreeColumnLayoutBlock,
    FourColumnLayoutBlock,
    ContentBlock,
    TextBlock,
    TitleTextBlock,
    PageNavigationBlock,
    PrimaryNavigationBlock,
    VideoBlock,
    TwitterBlock
)


from .product import (
    SingleProductBlock,
    HandPickedProductsPromotionBlock,
    AutomaticProductsPromotionBlock,
    OfferBlock,
)
