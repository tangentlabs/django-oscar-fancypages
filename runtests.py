#!/usr/bin/env python
import os
import sys
import logging
import tempfile
from optparse import OptionParser

from django.conf import settings

from oscar.defaults import OSCAR_SETTINGS
from oscar import OSCAR_MAIN_TEMPLATE_DIR, OSCAR_CORE_APPS

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MEDIA_ROOT=location('public/media'),
        MEDIA_URL='/media/',
        STATIC_URL='/static/',
        STATICFILES_DIRS=(location('static/'),),
        STATIC_ROOT=location('public'),
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ),
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'oscar.apps.basket.middleware.BasketMiddleware',
        ),
        ROOT_URLCONF='sandbox.sandbox.urls',
        TEMPLATE_DIRS=(
            location('templates'),
            os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ),
        FANCYPAGES_TEMPLATE_DIRS=[
            location('templates/fancypages/pages'),
        ],
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
        ] + OSCAR_CORE_APPS + [
            'model_utils',

            'fancypages',
        ],
        AUTHENTICATION_BACKENDS=(
            'oscar.apps.customer.auth_backends.Emailbackend',
            'django.contrib.auth.backends.ModelBackend',
        ),
        LOGIN_REDIRECT_URL='/accounts/',
        APPEND_SLASH=True,
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
                'PATH': tempfile.mkdtemp()+'/whoosh_index/',
            },
        },
        NOSE_ARGS=['-s', '--with-spec'],  #'--with-progressive'],
        **OSCAR_SETTINGS
    )

logging.disable(logging.CRITICAL)


def run_tests(*test_args):
    from django_nose import NoseTestSuiteRunner
    test_runner = NoseTestSuiteRunner(verbosity=1)
    if not test_args:
        test_args = ['tests']
    num_failures = test_runner.run_tests(test_args)
    if num_failures:
        sys.exit(num_failures)


if __name__ == '__main__':
    parser = OptionParser()
    options, args = parser.parse_args()
    run_tests(*args)
