# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Alberto Vara <a.vara.1986@gmail.com>
from setuptools import setup, find_packages
import codecs
import os

version = __import__('gozokia').__version__
author = __import__('gozokia').__author__
author_email = __import__('gozokia').__email__

if os.path.exists('README.rst'):
    long_description = codecs.open('README.md', 'r', 'utf-8').read()
else:
    long_description = 'See https://github.com/avara1986/gozokia'

setup(
    name="gozokia",
    version=version,
    author=author,
    author_email=author_email,
    description="",
    long_description=long_description,
    scripts=['gozokia/__main__.py'],
    classifiers=[
        'Development Status :: 0.2 - Beta',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'License :: MIT',
        "Environment :: Console",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    license="MIT",
    platforms=["any"],
    keywords="gozokia",
    url='https://github.com/avara1986/gozokia.git',
    test_suite='nose.collector',
    packages=find_packages(),
    include_package_data=True,
)
