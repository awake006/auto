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
    name="api",  # pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    version="1.7",
    author="xiaoming",
    author_email="hietel366435@163.com",
    description="Test API",
    license="GPLv3",
    keywords="TEST API",
    url="https://github.com/awake006",
    packages=['api'],  # 需要打包的目录列表

    # 需要安装的依赖
    # install_requires=[
    #     'redis>=2.10.5',
    #     'setuptools>=16.0',
    # ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'study = study.main:main',
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
