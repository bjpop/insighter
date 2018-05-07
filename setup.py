#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''Annotate DNA variants using the InSiGHT database'''


setup(
    name='insighter-py',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['insighter'],
    package_dir={'insighter': 'insighter'},
    entry_points={
        'console_scripts': ['insighter = insighter.insighter:main']
    },
    url='https://github.com/bjpop/insighter',
    license='LICENSE',
    description=('Annotate DNA variants using the InSiGHT database'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["feedparser"],
)
