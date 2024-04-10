#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import setup, find_packages


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='sparkproxy',
    version=find_version("sparkproxy/__init__.py"),
    description='Spark proxy OpenApi SDK',
    long_description='see:\nhttps://github.com/yungoo/spark-sdk-python\n',
    author='Spark Proxy Co., Ltd.',
    author_email='sdk@sparkproxy.com',
    maintainer_email='support@sparkproxy.com',
    license='MIT',
    url='https://github.com/yungoo/spark-sdk-python',
    platforms='any',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'requests; python_version >= "3.7"',
        'requests<2.28; python_version < "3.7"',
        'futures; python_version == "2.7"',
        'cryptography'
    ],
    extras_require={
        'dev': [
            'coverage<7.2',
            'flake8',
            'pytest',
            'pytest-cov',
            'freezegun',
            'scrutinizer-ocular',
            'codecov'
        ]
    },

    entry_points={
        'console_scripts': [
            'sparkproxypy = sparkproxy.main:main',
        ],
    }
)
