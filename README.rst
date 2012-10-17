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

