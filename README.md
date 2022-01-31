# CrossInstaller

[![Build](https://github.com/desty2k/crossinstaller/actions/workflows/build.yml/badge.svg)](https://github.com/desty2k/crossinstaller/actions/workflows/build.yml)
[![Version](https://img.shields.io/pypi/v/crossinstaller)](https://pypi.org/project/crossinstaller/)
[![Version](https://img.shields.io/pypi/dm/crossinstaller)](https://pypi.org/project/crossinstaller/)

Create Python executables for Linux and Windows using one command.

## Installation

From PyPI

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

### Creating executables

Target platforms are specified by the `--platform` option. Option can be specified multiple times.
At least one platform must be specified. Available default platforms are: `win32`, `win64`, `i386`, `amd64`.

```shell
crossinstaller some_script.py -p amd64 -p win64
```
The above command will create two executables: `some_script` for Linux x64 and `some_script.exe` for Windows x64.

### Adding custom platform
Use `-a`/`--add-platform` option to add custom platform. For example, if you want to create 
an executable for `platform_name` platform, which use `dockerfile` Dockerfile, you can do it like this:
```shell
crossinstaller some_script.py -a platform_name path/to/dockerfile
```
Option can be specified multiple times.

### Passing extra arguments to the Pyinstaller
You can pass extra arguments to the Pyinstaller by using `-e`/`--options` option. 
Make sure to quote the arguments. __Note the extra space in the argument.__
```shell
crossinstaller some_script.py --options " -F --icon icon.ico"
```

### Specifying the working directory
By default, the working directory is the same as the script directory. 
You can specify custom working directory by using `-w`/`--workdir` option.
```shell
crossinstaller path/to/some_script.py -w path/
```

### Using in a script
You can use crossinstaller as a Python module. Note that working directory will be changed to the script directory.

```python
from pathlib import Path
from crossinstaller import Platform, CrossInstaller, get_default_platforms

if __name__ == '__main__':
    generator = CrossInstaller()
    # add default platforms
    generator.add_platforms(get_default_platforms())
    # add custom platform
    # note: all files required by the Dockerfile must be in the same directory as the Dockerfile
    my_platform = Platform("my-platform-64", Path("/usr/bin/my-platform-64/Dockerfile"))
    generator.add_platform(my_platform)
    # start crossinstaller
    generator.start(Path("path/to/my/script.py"), keep_build=True, extra_options="-F")
    # start is non blocking, you can do other stuff here
    # or wait for the build to finish
    generator.wait()
```

