#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Package imports
from crossinstaller.config import __version__

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name='crossinstaller',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/desty2k/crossinstaller',
    license='MIT',
    author='Wojciech Wentland',
    author_email='wojciech.wentland@int.pl',
    description='PyInstaller + Docker = CrossInstaller',
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    zip_safe=False,  # don't use eggs
    long_description=long_desc,

    install_requires=['docker'],
    package_data={'': ['./Docker/*']},
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'crossinstaller=crossinstaller.__main__:main_entry',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',

        'Programming Language :: Python :: Implementation :: CPython',

        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',

        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',

    ],
    keywords=['packaging', 'app', 'apps', 'bundle', 'convert', 'standalone', 'executable',
              'pyinstaller', 'cxfreeze', 'freeze', 'py2exe', 'py2app', 'bbfreeze', 'docker'],
)
