from django.db.models import get_model

from fancypages import abstract_models
from fancypages.models import *

from .product import (
    SingleProductBlock,
    HandPickedProductsPromotionBlock,
    AutomaticProductsPromotionBlock,
    OfferBlock,
)

Category = get_model('catalogue', 'Category')


class FancyPage(Category, abstract_models.AbstractFancyPage):
        objects = PageManager()

        class Meta:
            app_label = 'fancypages'
