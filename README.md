# CrossInstaller

[![Build](https://github.com/desty2k/crossinstaller/actions/workflows/build.yml/badge.svg)](https://github.com/desty2k/crossinstaller/actions/workflows/build.yml)
[![Version](https://img.shields.io/pypi/v/crossinstaller)](https://pypi.org/project/crossinstaller/)
[![Version](https://img.shields.io/pypi/dm/crossinstaller)](https://pypi.org/project/crossinstaller/)

Create Python executables for Linux and Windows using one command.

## Installation

From PyPI (TODO)

```shell
pip install crossinstaller -U
```

From sources

```shell
git clone https://github.com/desty2k/crossinstaller.git
cd crossinstaller
pip install .
```

## Usage

By default, crossinstaller will build executables for win32, win64, i386, amd64.

```shell
crossinstaller build some_script.py
```
