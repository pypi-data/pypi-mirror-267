#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ____  _ _        _      ____  _  _     ____  _____ ____ _____
#  | __ )(_) |_ _ __(_)_  _|___ \| || |   |  _ \| ____/ ___|_   _|
#  |  _ \| | __| '__| \ \/ / __) | || |_  | |_) |  _| \___ \ | |
#  | |_) | | |_| |  | |>  < / __/|__   _| |  _ <| |___ ___) || |
#  |____/|_|\__|_|  |_/_/\_\_____|  |_|   |_| \_\_____|____/ |_|

"""
Setup file for Bitrix24 REST API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2019 by Akop Kesheshyan.
"""

from distutils.core import setup
from setuptools import find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bitrix24-rest-motexc',
    version='1.1.5',
    install_requires=['requests'],
    packages=find_packages(),
    url='https://github.com/Motexc/bitrix24-python-rest.git',
    license='MIT',
    author='Andrey Yakovlev',
    author_email='modifikator97@gmail.com',
    description="A fork of bitrix24-rest package, abandoned by it's author Akop Kesheshyan",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='bitrix24 api rest fork',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
)
