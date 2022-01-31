import os
import logging
from pathlib import Path
from threading import Thread

from crossinstaller.platform import Platform, get_default_platforms
from crossinstaller.generator import Generator

__all__ = ("CrossInstaller")


class CrossInstaller:

    def __init__(self):
        super(CrossInstaller, self).__init__()
        self._platforms: list[Platform] = []
        self._generators: list[(Generator, Thread)] = []

    def start(self, script_path: Path, workdir: Path, keep_build: bool = False, extra_options: str = ""):
        """Start the cross-compilation process."""
        # check if script exists
        if not script_path.is_file():
            raise FileNotFoundError(f"script {script_path} not found")
        # check if custom workdir is valid
        if workdir is not None:
            if not workdir.is_dir():
                raise FileNotFoundError(f"workdir {workdir} does not exist")
            if not script_path.is_relative_to(workdir):
                raise ValueError(f"script {script_path} is not in workdir {workdir}")
        else:
            workdir = script_path.parent
        # make sure we are in the script's directory
        os.chdir(workdir)
        try:
            import docker
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
        """Wait for all threads to finish."""
        for g, t in self._generators:
            t.join(timeout)

    def stop(self):
        """Stop all threads."""
        for g, t in self._generators:
            g.stopped = True

    def platforms(self):
        """Return a list of target platforms."""
        return self._platforms

    def add_platform(self, platform: Platform):
        """Add a target platform."""
        self._platforms.append(platform)

    def add_platforms(self, platforms: list[Platform]):
        """Add multiple target platforms."""
        self._platforms.extend(platforms)

    def remove_platform(self, platform: Platform):
        """Remove a target platform."""
        self._platforms.remove(platform)

    def is_running(self):
        """Return True if any thread is still running."""
        return any(not g.is_finished() for g, t in self._generators)
