import os
import time
import docker
import logging
import threading

from crossinstaller.generators import *
from crossinstaller.errors import CrossInstallerError

GENERATORS = [i386Generator, Amd64Generator, Win32Generator, Win64Generator]

__all__ = ["__version__", "crosscompile"]
__version__ = "0.0.2"


def crosscompile(script_path, keep_build=False):
    script_path = os.path.realpath(script_path)
    script_dir = os.path.dirname(script_path)
    if not os.path.isfile(script_path):
        raise CrossInstallerError("{} not a file".format(script_path))

    try:
        client = docker.from_env()
    except Exception as e:
        logging.error("Failed to instantiate Docker client: {}".format(e))
        raise e

    running_generators = []
    try:
        for generator in GENERATORS:
            gen_onj = generator(client, script_path, script_dir, keep_build=keep_build)
            gen_thr = threading.Thread(target=gen_onj.start)
            gen_thr.start()
            running_generators.append((gen_onj, gen_thr))

        while not all(gen.finished for gen, thr in running_generators):
            time.sleep(5)
    except KeyboardInterrupt:
        for gen, thr in running_generators:
            gen.stop()
            thr.join(10)
        logging.info("Operation cancelled by user")
