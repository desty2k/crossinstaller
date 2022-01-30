import os
import shutil


__all__ = ("CrossInstaller")

import docker
import logging
from pathlib import Path
from threading import Thread
from crossinstaller.platform import Platform, get_default_platforms
from crossinstaller.generator import Generator


class CrossInstaller:

    def __init__(self):
        super(CrossInstaller, self).__init__()
        self._platforms: list[Platform] = []
        self._generators: list[(Generator, Thread)] = []

    def start(self, script_path: Path, keep_build: bool = False, extra_options: str = ""):
        try:
            client = docker.from_env()
        except Exception as e:
            logging.error("Failed to instantiate Docker client: {}".format(e))
            raise e

        for platform in self._platforms:
            generator = Generator(client, platform, script_path, keep_build, extra_options)
            thread = Thread(target=generator.start)
            thread.start()
            self._generators.append((generator, thread))

    def wait(self, timeout=None):
        for g, t in self._generators:
            t.join(timeout)

    def stop(self):
        for g, t in self._generators:
            g.stopped = True

    def platforms(self):
        return self._platforms

    def add_platform(self, platform: Platform):
        self._platforms.append(platform)

    def add_platforms(self, platforms: list[Platform]):
        self._platforms.extend(platforms)

    def remove_platform(self, platform: Platform):
        self._platforms.remove(platform)

    def is_running(self):
        return any(not g.is_finished() for g, t in self._generators)
