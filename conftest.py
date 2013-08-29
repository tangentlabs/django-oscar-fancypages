import os

from django.conf import settings

from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import OSCAR_SETTINGS

import oscar_fancypages.utils as ofp_utils

from oscar_fancypages.defaults import FANCYPAGES_SETTINGS


location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
sandbox = lambda x: location("oscar_sandbox/%s" % x)


def pytest_configure():
    SETTINGS = OSCAR_SETTINGS
    SETTINGS.update(FANCYPAGES_SETTINGS)

    settings.configure(
        DEBUG=True,
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
            sandbox('static/')
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
            'fancypages.middleware.EditorMiddleware',
        ),
        ROOT_URLCONF='oscar_sandbox.sandbox.urls',
        TEMPLATE_DIRS=[
            sandbox('templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ] + ofp_utils.get_oscar_fancypages_paths('templates'),
        INSTALLED_APPS=[
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
            'django_extensions',
        ] + ofp_utils.get_oscar_fancypages_apps() + get_core_apps(),
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
        SITE_ID=1,
        **SETTINGS
    )
