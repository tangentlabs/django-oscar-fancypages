======================================
Fancy CMS-style page editing for Oscar
======================================

.. image:: https://travis-ci.org/tangentlabs/django-oscar-fancypages.png
    :target: https://travis-ci.org/tangentlabs/django-oscar-fancypages?branch=master

.. image:: https://coveralls.io/repos/tangentlabs/django-oscar-fancypages/badge.png?branch=master
    :target: https://coveralls.io/r/tangentlabs/django-oscar-fancypages?branch=master

Warning
-------

I just commited a bug fix that will break for existing projects using
django-oscar-fancypages as I had to regenerate the initial migration.  Since
this is an import issue and not an actual model change, I didn't see a way
around this via migrations. Sorry for any inconvenience.

**Keep in mind that this is still under development and breaking changes like
the one above are not unlikely. Use with care and hold off on that production
build until the first proper release.**


This Django app is an extension that integrates `django-fancypages`_ with
`django-oscar`_ and provides it's features as a content enhancement system to
Oscar. The *fancy pages* integrate with the category structure of Oscar by
wrapping around the ``ProductCategory`` model, plugging them into the
category tree of Oscar. As a result, the existing category structure is
available as fancy pages after installing ``django-oscar-fancypages`` (OFP) and
creating a fancypage creates a ``ProductCategory`` that can be used to
display products.

For more details on fancy pages refer to `django-fancypages`_


Installation
------------

Before installing OFP and use it with your project, make sure that you have
setup `django-oscar`_ properly. If you haven't done so, please check the
Oscar documentation for installation instructions. Come back here after you
have successfully set up your Oscar sandbox and follow these steps:

1. Install ``django-oscar-fancypages`` from the github repo using ``pip``.
   Currently there's no PyPI release available. To install run the
   following command::

    $ pip install git+https://github.com/tangentlabs/django-oscar-fancypages.git

2. Add all required third-party apps and the OFP apps to your
   ``INSTALLED_APPS``. There are convenience functions available to make
   it easier::

    import oscar_fancypages.utils as ofp_utils
    INSTALLED_APPS = [
        ...
    ] + ofp_utils.get_required_apps() + ofp_utils.get_oscar_fancypages_apps()

3. For all the static files and templates that are required from
   ``django-fancypages``, you have to add a couple of extra lines to
   make sure that these files can be overwritten locally by putting the
   search locations in the right order. Again, there's a convenience
   function available::

    TEMPLATE_DIRS = [
        ...
    ] + ofp_utils.get_oscar_fancypages_paths('templates')

    ...

    STATICFILES_DIRS = [
        ...
    ] + ofp_utils.get_oscar_fancypages_paths('static')

4. Next, you have to add the editor middleware that let's you access
   the editor panel on pages with a fancypage container::

    MIDDLEWARE_CLASSES = (
        ...
        'fancypages.middleware.EditorMiddleware',
    )

5. To hook up all the pages, the dashboard and the integrated asset manager
   you need to add the URL patterns to your project's ``urls.py``. The basic
   URLs can be included using::

    urlpatterns = patterns('',
        ...
        url(r'', include('oscar_fancypages.urls')),
    )

   Make sure that you add it **after** all your other pages to make sure that
   it only looks for OFP pages when all other lookups have failed. Otherwise
   you won't be able to see anything but OFP pages.

6. Finally, it makes sense to add all the default settings for OFP to
   your ``settings.py`` to prevent errors caused by missing settings, e.g.
   the twitter package does not allow unset API keys and tokens. Use
   the following at the end of your ``settings.py`` before overriding any
   of the settings::

    from oscar_fancypages.defaults import *

.. _`django-oscar`: https://github.com/tangentlabs/django-oscar
.. _`django-fancypages`: https://github.com/tangentlabs/django-fancypages

License
-------

``django-oscar-fancypages`` is released under the permissive
`New BSD license`_.

.. _`New BSD license`:
    https://github.com/tangentlabs/django-oscar-fancypages/blob/master/LICENSE



.. image:: https://d2weczhvl823v0.cloudfront.net/tangentlabs/django-oscar-fancypages/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

