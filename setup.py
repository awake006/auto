# -*- coding: utf-8 -*-
import ast
import os
import re
from setuptools import setup

# parse version from api / __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_init_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "auto", "__init__.py")
with open(_init_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name="auto",
    version=version,
    author="awake006",
    author_email="hietel366435@163.com",
    description="Interface automation test tool",
    license="MIT",
    keywords="",
    url="https://github.com/awake006/auto",
    packages=['auto'],
    install_requires=[
        'Flask>=1.0.2',
        'setuptools>=28.8.0',
        'lxml>=4.1.1',
        'PyMySQL>=0.8.1',
        'PyYAML>=3.12',
        'requests>=2.13.0',
        'xmlrunner>=1.7.7',
        'locustio>=0.8.1',
    ],


    entry_points={'console_scripts': [
        'auto = auto.main:main',
    ]},

    classifiers=[
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    zip_safe=False
)
