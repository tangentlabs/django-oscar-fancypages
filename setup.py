#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-oscar-fancypages',
    version=":versiontools:oscar_fancypages:",
    url='https://github.com/tangentlabs/django-oscar-fancypages',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Integrate fancypages CEnS into Oscar",
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('CHANGELOG.rst').read(),
    ]),
    keywords="django, oscar, e-commerce, cms, pages, flatpages",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'versiontools>=1.9.1',
        'django-oscar>=0.5',
        'django-fancypages>=0.1.0,<0.2',
    ],
    dependency_links=[
        'https://github.com/tangentlabs/django-fancypages/tarball/master#egg=django-fancypages-0.1.0'
    ],
    setup_requires=[
        'versiontools >= 1.8',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: Unix',
      'Programming Language :: Python',
    ])
