#!/usr/bin/env python

from setuptools import setup, find_packages

from rested_users import VERSION


install_requires = [
    'flask-restplus',
    'uwsgi',
]

tests_require = [
    'nose'
]

config = {
    'description': 'A REST service to be used to store, fetch, and update user records.',
    'author': 'Jesse Gonzalez',
    'url': 'https://github.com/jessegonzalez/rested_users',
    'author_email': 'jesse.gonzalez.jr@gmail.com',
    'version': VERSION,
    'install_requires': install_requires,
    'tests_require': tests_require,
    'test_suite': 'nose.collector',
    'packages': ['rested_users'],
    'scripts': [],
    'name': 'rested_users'
}

setup(**config)
