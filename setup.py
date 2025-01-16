#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#with open('requirements.txt', 'r') as f:
#    requirements = f.read().splitlines()


if __name__ == '__main__':
    setup(
        name='chris_tools',
        version='1.0.0',
        description='',
        author='',
        author_email='qhrisj@gmail.com',
        #include_package_data=True,
        #packages='database',
        #install_requires=requirements,
        )
