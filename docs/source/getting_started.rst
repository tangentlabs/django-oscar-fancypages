Getting Started
===============

The basic idea behind ``django-oscar-fancypages`` is to provide a user-friendly
and easy way to add custom content to `django-oscar`_. This sounds like yet
another content management system (CMS) and why would we need that? The reason
is that fancypages is **not** a CMS but more of a content enhancement system.
It provides a user with the flexibility of creating and organising arbitrary
content within their Oscar system without interfering with the site's design
guidelines, its responsiveness and basic catalogue structure. 

The concept
-----------

Fancypages provides *four* major elements that allow the composition of
(almost) any content:

1. Containers
2. Object(-related) containers
3. Pages
4. Widgets

The general structure of this elements is that a *page* represents a custom
webpage with its own URL. The basic layout of a page is defined by a page type
which provides a way of using different templates for different pages. 

Any django template - not only of a *page* - can have one or more *containers*
placed in it and will give a user the ability to add widgets at the specified
location. The different between a basic container and an object-related 
container is explained below. 

The last element is the *widget* which comes in various shapes and forms
(althought they are all rectangular). They provide the means to add actual 
content and place it in container. There are also *layout* containers that
allow a user to split a container into a multi-column layout and place widgets
in each of these columns. Fancypages comes with a variety of built-in widgets
but also makes it very easy to create your own project-specific widgets. This
is explained in `howto create a custom widget`.

A simplified structure of a page could look like this::

            +---------------------------------------------+
            | An author page                              |
            |                                             |
            | +-----------------------------------------+ |
            | |A container                              | |
            | |+---------------------------------------+| |
            | ||Text widget: a short description of the|| |
            | ||  authours career.                     || |
            | |+---------------------------------------+| |
            | +-----------------------------------------+ |
            |                                             |
            | Here is some content that is                |
            | defined in the template and                 |
            | cannot be altered through                   |
            | fancypages, e.g. a list of                  |
            | products by this author                     |
            |                                             |
            | +-----------------------------------------+ |
            | |Another container                        | |
            | |+---------------------------------------+| |
            | ||Video widget: a youtube video of a TED || |
            | ||  talk by the author                   || |
            | |+---------------------------------------+| |
            | |+---------------------------------------+| |
            | ||Twitter widget: pull in the latest     || |
            | ||  tweets by the author                 || |
            | |+---------------------------------------+| |
            | +-----------------------------------------+ |
            +---------------------------------------------+


The elements that make up fancypages
------------------------------------

The following will go into more detail describing the individual elements that
are used to make up fancypages. 

The basic container
++++++++++++++++++

The idea of a container is very simple. It is an element that is placed in a
template and can *contain* an arbitrary number of widgets. A container is
identified by a **name** and this names is unique within the Oscar site. A
container is placed in a template by referencing its name.  

Consequently, placing a container with the same name in multiple templates will
**always** display the same content. Playing a container in a template is 
as simple as adding the appropriate template tag::

    {% load fp_container_tags %}
    ...
    {% fp_container my-container-name %}


The object-related container
++++++++++++++++++++++++++++

An object-related container is a more specific type of container to the one
explained before. In addition to a **name**, this container requires a model
instance (object) that it is related to. As an example, we can attach a
container to a specific product by placing it in the template for an individual
product::

    {% load fp_container_tags %}
    ...
    {% fp_object_container my-container-name %}

This will create a container for each product, assuming that it is available
in the template context as ``object``. It can also be specified explicitly::

    {% load fp_container_tags %}
    ...
    {% fp_object_container my-container-name product %}

The widgets placed inside an object-related container will only be displayed
on the page of the object they are related to. This means a user can create
specific additional content for one product and it will only be displayed on
that product's detail page.

The (fancy) page
++++++++++++++++

Pages in fancypages are a broader interpretation of the Oscar's ``Category``. 
In fact you can think of them as being the same thing entirely. That means you
can have products associtated with a page as you would with a category.

A page has an absolute URL by which it is identified on the page. The
way it looks and the type of content displayed depends on the *page type* that
you select for it. You could create a "Fancypage" which will give you a blank
slate and leaves the whole design of the page up to you. Or you could make it
a "Product list page" which will display all the products that are in this
page/category. On top of that, it will give you several containers on the page
where you can add your widgets.

The widget
++++++++++

The widget is the most powerful element of them all and can range from a very
simple *text widget* to complex, context-sensitive widgets that display the 
most viewed products in a given category. These widgets are *content* widgets.
To provide more flexibility, there are also *layout* widgets that allow you to
split a container into a multi-column layout. 

As previously stated, fancypages comes with a broad selection of built-in
widgets but makes it easy to create custom widgets for your projects.


.. _`django-oscar`: http://www.oscarcommerce.com
