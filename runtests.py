#!/usr/bin/env python
import os
import sys
import logging
import tempfile

from argparse import ArgumentParser

from django.conf import settings

from oscar.defaults import OSCAR_SETTINGS
from fancypages.defaults import FANCYPAGES_SETTINGS
from oscar import OSCAR_MAIN_TEMPLATE_DIR, OSCAR_CORE_APPS

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
sandbox = lambda x: location("sandbox/%s" % x)


def configure():
    if not settings.configured:
        OSCAR_SETTINGS.update(FANCYPAGES_SETTINGS)
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            MEDIA_ROOT=sandbox('public/media'),
            MEDIA_URL='/media/',
            STATIC_URL='/static/',
            STATICFILES_DIRS=(sandbox('static/'),),
            STATIC_ROOT=sandbox('public'),
            STATICFILES_FINDERS=(
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                'compressor.finders.CompressorFinder',
            ),
            TEMPLATE_LOADERS=(
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
            TEMPLATE_CONTEXT_PROCESSORS = (
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.request",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                # Oscar specific
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ),
            MIDDLEWARE_CLASSES=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'debug_toolbar.middleware.DebugToolbarMiddleware',
                'oscar.apps.basket.middleware.BasketMiddleware',
                'fancypages.middleware.EditorMiddleware',
            ),
            ROOT_URLCONF='sandbox.sandbox.urls',
            TEMPLATE_DIRS=(
                sandbox('templates'),
                os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
                OSCAR_MAIN_TEMPLATE_DIR,
            ),
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
                'compressor',
                'fancypages',
                'fancypages.assets',
                'twitter_tag',
                'model_utils',
            ] + OSCAR_CORE_APPS + [
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
            NOSE_ARGS=[
                '-s',
                '--with-spec',
            ],
            **OSCAR_SETTINGS
        )

logging.disable(logging.CRITICAL)


def run_tests(verbosity=1, *test_args):
    from django_nose import NoseTestSuiteRunner
    test_runner = NoseTestSuiteRunner(verbosity=verbosity)
    if not test_args:
        test_args = ['tests']
    num_failures = test_runner.run_tests(test_args)
    if num_failures:
        sys.exit(num_failures)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-v', default=1, dest='verbosity', type=int,
                        help="Set verbosity of nose test runner [default: 1]")
    args, remaining_args = parser.parse_known_args()
    configure()
    run_tests(args.verbosity, *remaining_args)
