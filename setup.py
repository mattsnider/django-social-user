#!/usr/bin/env python
import os

# python setup.py sdist bdist_wininst upload

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# README is required for distribution, but README.md is required for github,
#   so create README temporarily
os.system('cp %s/README.md %s/README.txt' % (ROOT_DIR, ROOT_DIR))

sdict = dict(
    name = 'django-social-user',
    packages = ['django_social_user', 'django_social_user.migrations'],
    version='.'.join(map(str, __import__('django_social_user').__version__)),
    description = 'A generic system for interacting with remote APIs '
                  'that need to create Django users.',
    long_description=open('README.md').read(),
    url = 'https://github.com/mattsnider/Django-Social-User',
    author = 'Matt Snider',
    author_email = 'admin@mattsnider.com',
    maintainer = 'Matt Snider',
    maintainer_email = 'admin@mattsnider.com',
    keywords = ['social', 'user'],
    license = 'MIT',
    install_requires=['django>=1.3'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)

# if setup tools are available, package using setup tools
# otherwise use default
try:
    from setuptools import setup
    setup(**sdict)
except ImportError:
    # install_requires is not a valid key for default distutils
    from distutils.core import setup
    sdict.pop("install_requires", None)
    setup(**sdict)

# cleanup README
os.remove('%s/README.txt' % ROOT_DIR)