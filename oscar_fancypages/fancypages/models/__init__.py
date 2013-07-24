from __future__ import absolute_import

from django.db.models import get_model

from fancypages import manager
from fancypages import abstract_models

Category = get_model('catalogue', 'Category')


class FancyPage(Category, abstract_models.AbstractFancyPage):
    objects = manager.PageManager()


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
