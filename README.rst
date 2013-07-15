======================================
Fancy CMS-style page editing for Oscar
======================================

This Django app is an extension that integrates `django-fancypages`_ with
`django-oscar`_ and provides it's features as a content enhancement system to
Oscar. The *fancy pages* integrate with the category structure of Oscar by
wrapping around the ``ProductCategory`` model, plugging them into the
category tree of Oscar. As a result, the existing category structure is
available as fancy pages after installing ``django-oscar-fancypages`` and
creating a fancypage creates a ``ProductCategory`` that can be used to 
display products.

For more details on fancy pages refer to `django-fancypages`_

.. _`django-fancypages`: https://github.com/tangentlabs/django-fancypages


License
-------

``django-oscar-fancypages`` is released under the permissive
`New BSD license`_.

.. _`New BSD license`:
https://github.com/tangentlabs/django-oscar-fancypages/blob/master/LICENSE
