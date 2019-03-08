# -*- coding: utf-8 -*-

import codecs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

desc = codecs.open('README.md', 'r', 'utf-8').read()

setup(
    name="nextt",
    url="",
    version= "1.0.0",
    description=desc,
    long_description=desc,
    license='BSD',
    author="NeverSayNever",
    author_email="15731114118@163.com",
    platforms='any',
)
