import os
import json
import time
import docker
import shutil
import logging
import threading

from crossinstaller.platform import Platform
from crossinstaller.generator import Generator
from crossinstaller.errors import CrossInstallerError

CROSSINSTALLER_DIRECTORY = os.path.dirname(__file__)
BUILD_DIRECTORY = os.path.join(CROSSINSTALLER_DIRECTORY, "./build/")
IMAGES_DIRECTORY = os.path.join(CROSSINSTALLER_DIRECTORY, "./Docker/")
PLATFORM_FILE = os.path.join(IMAGES_DIRECTORY, "platforms.json")

__all__ = ["__version__", "build", "load_platforms", "add_platform", "save_platforms"]
__version__ = "0.0.4"


def load_platforms():
    with open(PLATFORM_FILE, "r") as f:
        platforms_dict: dict = json.load(f)
    platforms = []
    for key, value in platforms_dict.items():
        platforms.append(Platform(key, value["image"], extra_files=value["extra_files"]))
    return platforms


def save_platforms(platforms: list[Platform]):
    platforms_dict = {}
    platforms_files = ["platforms.json"]
    for platform in platforms:
        platforms_dict[platform.name] = {"image": platform.image, "extra_files": platform.extra_files}
        platforms_files += [platform.image] + platform.extra_files
    with open(PLATFORM_FILE, "w+") as f:
        json.dump(platforms_dict, f, indent=4)
    for file in os.listdir(IMAGES_DIRECTORY):
        if file not in platforms_files:
            os.remove(file)


def add_platform(name, image, extra_files=None, overwrite=False):
    platforms = load_platforms()
    if any(platform.name == name for platform in platforms) and overwrite is False:
        raise ValueError("Platform '{}' already exists. Use --overwrite / -O to overwrite existing platform.")
    for platform in platforms:
        if platform.image == image:
            raise ValueError("Image '{}' is already being used by '{}' platform.".format(image, platform.name))
    for platform in platforms:
        for file in extra_files:
            if file in platform.extra_files:
                raise ValueError("Extra file '{}' already exists and is used by '{}' platform.".format(file,
                                                                                                       platform.name))
    shutil.copy2(image, IMAGES_DIRECTORY)
    for file in extra_files:
        shutil.copy2(file, IMAGES_DIRECTORY)
    platforms.append(Platform(name, image, extra_files))
    save_platforms(platforms)


def build(script_path, extra_options=None, keep_build=False):
    script_path = os.path.realpath(script_path)
    script_name = os.path.basename(script_path)
    script_dir = os.path.dirname(script_path)
    if not os.path.isfile(script_path):
        raise CrossInstallerError("{} not a file".format(script_path))
    if extra_options is None:
        extra_options = ""

    try:
        client = docker.from_env()
    except Exception as e:
        logging.error("Failed to instantiate Docker client: {}".format(e))
        raise e

    running_generators = []
    try:
        for platform in load_platforms():
            gen_obj = Generator(client, script_name, script_dir, platform.name,
                                platform.image, keep_build, extra_options)
            gen_thr = threading.Thread(target=gen_obj.start)
            gen_thr.start()
            running_generators.append((gen_obj, gen_thr))

        while not all(gen.finished for gen, thr in running_generators):
            time.sleep(5)
    except KeyboardInterrupt:
        for gen, thr in running_generators:
            gen.stop()
            thr.join(10)
        logging.info("Operation cancelled by user")
    if not keep_build:
        shutil.rmtree(BUILD_DIRECTORY, ignore_errors=True)
