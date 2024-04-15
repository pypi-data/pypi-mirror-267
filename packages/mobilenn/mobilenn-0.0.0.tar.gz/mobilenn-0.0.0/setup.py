from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from distutils.cmd import Command
from wheel.bdist_wheel import bdist_wheel

import platform
import glob

import py_compile
import os

import pdb


python_version = [int(x) for x in platform.python_version().split('.')]


with open('README.md', 'r', encoding='utf-8') as f:
    readme_md = f.read()

# get version
version = "0.0.0"


setup(
    name='mobilenn',
    version=version,
    author='hhq',
    author_email='hhq@zhidaoauto.com',
    description='nn light',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['torch>=1.9.0', 'tensorrt>=7.0', 'graphviz'],
    python_requires=">={0}.{1}, <{0}.{2}".format(python_version[0], python_version[1], python_version[1] + 1)
)
