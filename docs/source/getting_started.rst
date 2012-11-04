Getting Started
===============

The basic idea behind fancypages is to provide an easy way to 
edit content in the Oscar e-commerce platform based on a
visual-centric editing approach. A fancypage is based on a 
Django template that specifies one or more **containers** which
in turn can contain **widgets**. Whenever a new page is created
the underlying template is evaluated and if the specified
containers do not exists, they are created for the page.

Opening a page in *edit mode* will display the containers in
their respective places and provides additional editing controls
to add, update and remove **widgets**. There are many widgets
that come pre-defined with fancypages, however, you are not 
limited to the ones that are already there. Extending widgets
is simple and you can easily add your own personal flavour 
of widgets.

In the following chapters I will try and explain the structure
of each individual model used in assembling a fanypage, define
terms used to describe them and possible pitfalls in using
them.

Fancy Pages
-----------

A fancypage is structure based on a Django template that
defines one or more container locations. Each of these
locations allow you to add and update widgets into the
page and move them within and even in between containers. 

Containers are defined in the page's template using a 
specific template tag. A container definition in a template
might look like this::

    {% load fancypages_tags %}

    <html>
        <body>
            <div class="content">
                {% fancypages-container main-content %}
            </div>
        </body>
    </html>

This is a very simple template but illustrates the way a
container location is defined.

Whenever a new page is created, the template assigned
to the page by the ``PageType`` is evaluated and each
``fancypages-container`` tag is results in creating a
container to be created for this page.

The name ``main-content`` passed to the template tag is
the variable name that is used for the container and allows
for looking up and rendering containers.


Rendering a container
---------------------

When rendering the a fancypage, the ``fancypages-container``
template tag is processed by the template engine as it would
any other template tag. The template tag will lookup try and
render a container with the given variable name in two 
ways:

    1. It looks up the template variable in the context with the variable
        name passed into the template tag
    2. If no variable with this name can be found in the context it attempts
       to find a ``object`` variable in the context and searches for the
       given variable name in all of the object's containers.

In accordance with the behaviour of the Django templating 
system, the template tag will silently fail if none of the 
above methods succeed. This means no container and therefore
none of its widgets will be displayed.

With the right container variable passed into the template it will render
all the container's widgets using the render function of each which.


Rendering widgets
-----------------

Each widget provides a ``render`` method that is inherited from the base class



The fancypages CMS interface consists of several objects that
can be assembled into editable pages. The most basic object 
is the ``PageTemplate`` object that defines an actual Django
template to be used with a fancy page. A template specified 
in a ``PageTemplate`` requires a path to the template file
that is relative to your project's template directories.
Finding the template relies on the Django template engine and
therefore works in the same way as any other template.

With a page template defined, let's say you specify the template
to be ``fancypages/pages/article_page.html``, you can now use
this template to define various page types. A page type is 
modelled as ``PageType`` which uses a page template. An example
is a page type **Article** that is based on our previously 
defined template. We are now ready to create new pages of type
**Article**.

A fancy ``Page`` is the actual page displayed in Oscar. It 
contains metadata related to the page itself and a list of 
containers that manage the various places in the template
that can contain ``Widget``s. 




Installation
------------


Set up a project
----------------

Setting up a new Oscar project that uses fancypages is 


Defining page templates
-----------------------

Fancypages uses a template tag to define the location of 


Basics
======

This chapter explains the basic structure of fancypages and
how to use it within your own project setting up page
templates, create pages and add widgets to them.


The structure of pages
----------------------
