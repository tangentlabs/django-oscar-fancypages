#!/usr/bin/env python
import os
import sys
import logging

from argparse import ArgumentParser

from django.conf import settings

from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import OSCAR_SETTINGS

import oscar_fancypages.utils as ofp_utils

from oscar_fancypages.defaults import FANCYPAGES_SETTINGS

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
sandbox = lambda x: location("sandbox/%s" % x)


def configure():
    if not settings.configured:

        SETTINGS = OSCAR_SETTINGS
        SETTINGS.update(FANCYPAGES_SETTINGS)
        # now we are adding our own specific settings for the tests
        SETTINGS.update(dict(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            MEDIA_ROOT=sandbox('public/media'),
            MEDIA_URL='/media/',
            STATIC_URL='/static/',
            STATICFILES_DIRS=[
                sandbox('static/'),
            ] + ofp_utils.get_oscar_fancypages_paths('static'),
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
            ),
            MIDDLEWARE_CLASSES=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'debug_toolbar.middleware.DebugToolbarMiddleware',
                'fancypages.middleware.EditorMiddleware',
            ),
            ROOT_URLCONF='sandbox.sandbox.urls',
            TEMPLATE_DIRS=[
                sandbox('templates'),
                OSCAR_MAIN_TEMPLATE_DIR,
            ] + ofp_utils.get_oscar_fancypages_paths('templates'),
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',

                'model_utils',
                'compressor',
                'twitter_tag',
                'sorl.thumbnail',
                'rest_framework',
            ) + ofp_utils.get_oscar_fancypages_apps() + tuple(get_core_apps([])),
            AUTHENTICATION_BACKENDS=(
                'django.contrib.auth.backends.ModelBackend',
            ),
            HAYSTACK_CONNECTIONS={
                'default': {
                    'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
                },
            },
            LOGIN_REDIRECT_URL='/accounts/',
            APPEND_SLASH=True,
            NOSE_ARGS=[
                '-s',
                '--with-specplugin',
            ],
        ))
        settings.configure(**SETTINGS)

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
