======================================
Fancy CMS-style page editing for Oscar
======================================

Fancy pages is an extension to provide a Content Management System for Oscar Commerce which allows a site to be customised and built using widgets within any page of the website.

It is structured to allow widgets to be added to any page within an Oscar site without restriction. All pages created by fancy pages are in fact created as Oscar categories so are made available to the product navigation on the site.

.. image:: http://i.imgur.com/NWcEt.jpg?1
.. image:: http://i.imgur.com/giaYb.png

Current Functionality
=====================

A dashboard administrator can

* Create a new Page (category) in the site within a tree structure
* Manage the meta keywords for a page
* Manage whether a page is active or not
* Move pages within the tree structure via drag and drop
* Manage page visibility via start / end dates, and draft/published/archived status
* Preview a page within the site
* Add widgets to a page
* Alter the structure of a page using layout widgets
* Layout widgets can be nested to allow complete flexibility of the structure of a page
* Drag and drop widgets within a page

The following Widgets are currently shipped with fancy pages

Layout Widgets

* 2 Column widget - which can be split in proportion to the page
* 3 Column widget
* 4 column widget
* Tabbed content widget

Design Widgets

* Text
* Title + Text
* Image
* Image + Text

eCommerce Widgets

* Single Product Showcase
* Automatic Product Showcase
* Hand Picked Products Showcase
* Products within an offer showcase

3rd Party Plugin widgets

* Youtube
* Twitter


Planned Functionality
=====================

Fancy pages is still in active development with the following on the to do list. We dont feel its quite ready to be called a 0.1 release as there needs to be the following functionality added.

v0.1 Release

* A widget which displays all the products in the current and child categories in a list form which can be filtered. This is a must for e-commerce sites
* 

Beyond the 0.1 the roadmap is as follows

v0.2 Release

* Giving the users the ability to create "Master pages" so when a user creates a new page, they can choose from an existing layout with pre-created widgets and dummy data.
* A Facebook widget which pulls through the Facebook social plugin
* The ability to "copy" widgets and layouts
* A tidy up of the editing interface to make dragging and dropping of widgets easier
* A tidy up of the you tube widget to resize the video automatically
* A data capture widget which allows users to create forms
* Article snippets widget which can pull through summary data from another page / group of pages automatically
* Grouping of widgets together per widget type eg. Layout widgets, 3rd Party widgets
* Adding much needed documentation for getting started with fancy pages and how to create your first widget

v0.3 Release

* A re-write of the Fancy pages tree structure and administration to provide a better user experience of creating and managing the site.
* Front end improvements for multi site configuration - having the ability to target pages / widgets per different sites.
* General improvements to the Assets library to allow filtering of assets on sites with many

Running the sandbox
===================

Follow the following steps to setup the sandbox and run a sample
shop with fancy pages enabled::

    $ git clone git@github.com:elbaschid/django-oscar-fancypages.git
    $ cd django-oscar-fancypages
    $ mkvirtualenv fancypages

Then run::

    $ make sandbox

This will install dependencies, create the database and load some fixtures.

.. important:: Fancypages uses `django-compressor`_ to compile the ``less`` files
    on the fly when ``DEBUG = True`` and can use the ``compress`` management
    command to generate the ``css`` files during deployment (please refer to
    the `django-compressor`_ documentation for more details.

    Because of this, `node.js`_ and `less`_ are requirements to run the sandbox
    if you have both of them installed you don't have to worry. Otherwise, you'll
    have to install them manually or use the provided requirements file to
    install them into you virtual environment. To do that run::

      $ pip install -r requirements_compress.txt

    This will install a compiled version of `node.js`_ inside your virtualenv
    alongside with less and a ``lessc`` executable.

.. _`node.js`: http://nodejs.org
.. _`less`: http://lesscss.org
.. _`django-compressor`: http://django_compressor.readthedocs.org/en/latest/

The credentials for the superuser are::

    username: admin
    email: admin@tangentsnowball.com.au
    password: admin

Now run the server and you are done::

    $ ./manage.py runserver

Your are now able to view the page manager in the dashboard:

    http://localhost:8000/dashboard/fancypages/

or edit the included sample page here:

    http://localhost:8000/dashboard/fancypages/customise/1/


Note
----

There's currently no page overview/list outside of the dashboard that can
be used to access the rendered page as a customer would see it. The sample
page included in the fixture can be found here:

    http://localhost:8000/page/a-new-article/


Setting up your own project
===========================

Add  fancypages to your ``INSTALLED_APPS`` in the settings file and make
sure that ``django-compressor`` is there as well::

    INSTALLED_APPS = [
        ...
        'compressor',
        'fancypages',
        ...
    ]

Specify the directories to search for custom page templates in the 
``FANCYPAGES_TEMPLATE_DIRS`` settings and add it to your usual list
of template directories::

    FANCYPAGES_TEMPLATE_DIRS = [
        'templates/myfancypages',
    ]
    TEMPLATE_DIRS = [
        'templates',
        os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
        OSCAR_MAIN_TEMPLATE_DIR,
    ] + FANCYPAGES_TEMPLATE_DIRS

Finally, configure your ``urls.py`` to find the pages and the fancypages
dashboard. It could look something like this::

    urlpatterns = patterns('',
        ...
        url(r'^', include(fancypages_app.urls)),
        url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
        ...
    )
