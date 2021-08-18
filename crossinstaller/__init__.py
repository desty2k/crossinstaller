import os
import sys
import time
import docker
import logging
import threading

from crossinstaller.generators import *

GENERATORS = [i386Generator, Amd64Generator, Win32Generator, Win64Generator]

__all__ = ["__version__", "crosscompile"]
__version__ = "0.0.1"


def crosscompile(script, directory=None, keep_build=False, console=True):
    try:
        client = docker.from_env()
    except Exception as e:
        logging.error("Failed to instantiate Docker client: {}".format(e))
        raise e

    try:
        if not os.path.exists("./build/"):
            os.makedirs("./build/", exist_ok=True)
    except Exception as e:
        sys.exit(1)

    running_generators = []

    try:
        for generator in GENERATORS:
            gen_onj = generator(client, "\"ls\"", keep_build=keep_build)

            gen_thr = threading.Thread(target=gen_onj.start)
            gen_thr.start()
            running_generators.append((gen_onj, gen_thr))

        while not all(gen.finished for gen, thr in running_generators):
            time.sleep(5)
    except KeyboardInterrupt:
        for gen, thr in running_generators:
            gen.stop()
            thr.join(10)
        logging.info("Operation cancelled")
