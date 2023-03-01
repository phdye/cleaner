# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

import re

_version = re.search("^__version__\s*=\s*'(.*)'",
                     open('cleaner/__init__.py').read(),
                     re.M ).group(1)

# with open('README.rst', 'rb') as f:
#     _long_description = f.read().decode('utf-8')

with open('README.rst', 'r') as f:
    _long_description = f.read()

setup(
    name = 'cleaner',
    version = _version,
    description = "Cleaner searches for temporary files which may be deleted, a la niftyclean",
    author = 'Philip H. Dye',
    author_email = 'philip@phd-solutions.com',
    # url = 'http://www.phd-solutions.com/philip-d-dye',
    long_description = _long_description,
    packages = ['cleaner'],
    entry_points = {
        'console_scripts': ['cleaner = cleaner:main']
        },
)
