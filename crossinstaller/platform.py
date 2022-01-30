import sys
import inspect
from pathlib import Path

import crossinstaller


def is_default_platform_subclass(platform: type):
    """Check if object is a class that is a subclass of the default platform class."""
    return isinstance(platform, type) and issubclass(platform, DefaultPlatform) and platform != DefaultPlatform


def get_default_platforms() -> list["DefaultPlatform"]:
    """Get all default platform classes."""
    return [m() for n, m in inspect.getmembers(sys.modules[__name__], is_default_platform_subclass)]


def get_platform_by_name(name: str) -> "DefaultPlatform":
    """Get default platform class by name."""
    for platform in get_default_platforms():
        if platform.name == name:
            return platform


class Platform:
    """Represents a platform."""

    def __init__(self, name: str, dockerfile: Path):
        super(Platform, self).__init__()

        self.name = name
        self.dockerfile = dockerfile
        self.path = dockerfile.parent


class DefaultPlatform(Platform):

    def __init__(self, dockerfile: str):
        super(DefaultPlatform, self).__init__(self.__class__.__name__,
                                              Path(crossinstaller.__file__).parent / "Docker" / dockerfile)


class win32(DefaultPlatform):
    def __init__(self):
        super(win32, self).__init__("Dockerfile-py3-win32")


class win64(DefaultPlatform):
    def __init__(self):
        super(win64, self).__init__("Dockerfile-py3-win64")


class i386(DefaultPlatform):
    def __init__(self):
        super(i386, self).__init__("Dockerfile-py3-i386")


class amd64(DefaultPlatform):
    def __init__(self):
        super(amd64, self).__init__("Dockerfile-py3-amd64")
