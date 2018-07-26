# -*- coding: utf-8 -*-
import ast
import os
import re
from setuptools import setup

# parse version from api / __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_init_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "api", "__init__.py")
with open(_init_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name="api", 
    version=version,
    author="xiaoming",
    author_email="hietel366435@163.com",
    description="Test API",
    license="GPLv3",
    keywords="TEST API",
    url="https://github.com/awake006/APIAutoTest",
    packages=['api'],
    install_requires=[
        'XlsxWriter>=0.9.8',
        'setuptools>=28.8.0',
        'lxml>=4.1.1',
        'PyMySQL>=0.8.1',
        'PyYAML>=3.12',
        'requests>=2.13.0',
    ],


    entry_points={'console_scripts': [
        'api = api.main:main',
    ]},

    classifiers=[  
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False
)
