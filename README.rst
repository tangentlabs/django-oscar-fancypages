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

Then install all the requirements::

    $ python setup.py develop
    $ pip install -r requirements.txt

Now change into the sandbox directory and create the sample database
to use for fancypages::

    $ cd sandbox
    $ ./manage.py syncdb --noinput
    $ ./manage.py migrate

And finally, load some sample data into the database including a 
superuser::

    $ ./manage.py loaddata fixtures/auth.json
    $ ./manage.py loaddata fixtures/fancypages.json

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

