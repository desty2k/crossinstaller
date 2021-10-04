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

from crossinstaller import __version__, PLATFORM_FILE, IMAGES_DIRECTORY, BUILD_DIRECTORY


def clear_platforms():
    return save_platforms([])


def load_platforms():
    with open(PLATFORM_FILE, "r") as f:
        platforms_dict: dict = json.load(f).get("platforms", {})
    platforms = []
    for key, value in platforms_dict.items():
        platforms.append(Platform(key, value["image"], extra_files=value["extra_files"]))
    return platforms


def save_platforms(platforms: list[Platform]):
    original_wd = os.getcwd()
    os.chdir(IMAGES_DIRECTORY)
    platforms_dict = {"version": __version__, "platforms": {}}
    platforms_files = ["platforms.json"]
    for platform in platforms:
        platforms_dict["platforms"][platform.name] = {"image": platform.image, "extra_files": platform.extra_files}
        platforms_files += [platform.image] + platform.extra_files
    with open(PLATFORM_FILE, "w+") as f:
        json.dump(platforms_dict, f, indent=4)
    for file in os.listdir(IMAGES_DIRECTORY):
        if file not in platforms_files:
            os.remove(file)
    os.chdir(original_wd)
    return platforms


def add_platform(name, image, extra_files=None, overwrite=False):
    image = os.path.basename(image)
    extra_files = [os.path.basename(file) for file in extra_files]

    platforms = load_platforms()
    if any(platform.name == name for platform in platforms) and overwrite is False:
        raise ValueError("Platform '{}' already exists. Use --overwrite / -O to overwrite existing platform."
                         .format(name))
    # for platform in platforms:
    #     if platform.image == image and overwrite is False:
    #         raise ValueError("Image '{}' is already being used by '{}' platform.".format(image, platform.name))
    # for platform in platforms:
    #     for file in extra_files:
    #         if file in platform.extra_files:
    #             raise ValueError("Extra file '{}' already exists and is used by '{}' platform.".format(file,
    #                                                                                                    platform.name))
    for file in extra_files:
        shutil.copy2(os.path.realpath(file), IMAGES_DIRECTORY)
    platforms.append(Platform(name, image, extra_files))
    return save_platforms(platforms)


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
