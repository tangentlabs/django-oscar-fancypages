======================================
Fancy CMS-style page editing for Oscar
======================================

This Django app is an extension that integrates `django-fancypages`_ with
`django-oscar`_ and provides it's features as a content enhancement system to
Oscar. The *fancy pages* integrate with the category structure of Oscar by
wrapping around the ``ProductCategory`` model, plugging them into the
category tree of Oscar. As a result, the existing category structure is
available as fancy pages after installing ``django-oscar-fancypages`` (OFP) and
creating a fancypage creates a ``ProductCategory`` that can be used to 
display products.

For more details on fancy pages refer to `django-fancypages`_

.. _`django-fancypages`: https://github.com/tangentlabs/django-fancypages

Installation
------------

Before installing OFP and use it with your project, make sure that you have
setup `django-oscar`_ properly. If you haven't done so, please check the
Oscar documentation for installation instructions. Come back here after you
have successfully set up your Oscar sandbox and follow these steps:

    1. Install ``django-oscar-fancypages`` from the github repo using ``pip``.
        Currently there's no PyPI release available. To install run the
        following command::

        $ pip install git+https://github.com/tangentlabs/django-oscar-fancypages/tarball/master

    2. Add all required third-party apps and the OFP apps to your
        ``INSTALLED_APPS``. There are convenience functions available to make
        it easier::

        import oscar_fancypages as ofp
        INSTALLED_APPS = (
            ...
        ) + ofp.get_required_apps() + ofp.get_oscar_fancypages_apps()

    3. For all the static files and templates that are required from
        ``django-fancypages``, you have to add a couple of extra lines to
        make sure that these files can be overwritten locally by putting the
        search locations in the right order. Again, there's a convenience
        function available::

        TEMPLATE_DIRS = [
            ...
        ] + ofp.get_oscar_fancypages_paths('templates')

        ...

        STATICFILES_DIRS = [
            ...
        ] + ofp.get_oscar_fancypages_paths('static')

    4. Next, you have to add the editor middleware that let's you access
        the editor panel on pages with a fancypage container::

        MIDDLEWARE_CLASSES = (
            ...
            'fancypages.middleware.EditorMiddleware',
        )

    5. Finally, it makes sense to add all the default settings for OFP to
        your ``settings.py`` to prevent errors caused by missing settings, e.g.
        the twitter package does not allow unset API keys and tokens. Use
        the following at the end of your ``settings.py`` before overriding any
        of the settings::

        from oscar_fancypages.defaults import *

.. _`django-oscar`: https://github.com/tangentlabs/django-oscar


License
-------

``django-oscar-fancypages`` is released under the permissive
`New BSD license`_.

.. _`New BSD license`:
https://github.com/tangentlabs/django-oscar-fancypages/blob/master/LICENSE
