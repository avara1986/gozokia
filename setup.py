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
    name="Gozokia",
    version=version,
    author=author,
    author_email=author_email,
    description="",
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    license="MIT",
    keywords="gozokia",
    url='https://github.com/avara1986/gozokia.git',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
)