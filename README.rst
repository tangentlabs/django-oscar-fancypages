Fancy CMS-style page editing for Oscar
======================================

This extension provides fancy page editing for Oscar.

Disclaimer
----------

This project is currently a better proof of concept and will most
likely break or not work. Please use with care until this message
disappears!!!

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
