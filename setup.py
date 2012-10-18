#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-oscar-fancypages',
    version=":versiontools:fancypages:",
    url='https://github.com/tangentlabs/django-oscar-fancypages',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Adding fancy CMS-style pages to Oscar",
    long_description=open('README.rst').read(),
    keywords="django, oscar, e-commerce, cms, pages, flatpages",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'versiontools>=1.9.1',
        'Django>=1.4.2',
        'django-oscar>=0.3',
        'django-model-utils>=1.1.0',
        'django-compressor>=1.2',
    ],
    dependency_links=[
        'http://github.com/tangentlabs/django-oscar/tarball/master#egg=django-oscar-0.4'
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      #'License :: OSI Approved :: BSD License',
      'Operating System :: Unix',
      'Programming Language :: Python'
    ]
)
