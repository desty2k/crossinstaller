import os

CROSSINSTALLER_DIRECTORY = os.path.dirname(__file__)
BUILD_DIRECTORY = os.path.join(CROSSINSTALLER_DIRECTORY, "build")
IMAGES_DIRECTORY = os.path.join(CROSSINSTALLER_DIRECTORY, "Docker")
PLATFORM_FILE = os.path.join(IMAGES_DIRECTORY, "platforms.json")

__all__ = ("__version__", "CROSSINSTALLER_DIRECTORY", "BUILD_DIRECTORY", "IMAGES_DIRECTORY", "PLATFORM_FILE")
__version__ = "0.1.0"
