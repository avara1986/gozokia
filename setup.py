# -*- coding: utf-8 -*-
# Copyright (c) 2016 by Alberto Vara <a.vara.1986@gmail.com>

import os
from setuptools import setup, find_packages

version = __import__('gozokia').__version__
maintainer = __import__('gozokia').__maintainer__
maintainer_email = __import__('gozokia').__email__

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="Gozokia",
    version=version,
    author=maintainer,
    author_email=maintainer_email,
    description="",
    long_description=(read('README.md')),
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