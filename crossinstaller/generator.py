import shutil
import logging
from pathlib import Path

from crossinstaller.platform import Platform


class Generator:

    def __init__(self, docker_client, platform: Platform, script_path: Path, keep_build: bool, extra_options: str):
        super(Generator, self).__init__()
        self.logger = logging.getLogger(f"crossinstaller-{platform.name}")

        self.docker_client = docker_client
        self.platform = platform
        self.container = None
        self.finished = False
        self.stopped = False
        self.scipt_path = script_path
        self.keep_build = keep_build

        self.platform.build_dir.mkdir(parents=True, exist_ok=True)
        self.platform.dist_dir.mkdir(parents=True, exist_ok=True)

        self.command = "\"ls && pyinstaller \'{}\' --workpath {} --specpath {} --distpath {} {}\"".format(
            script_path.name,
            self.platform.build_dir.as_posix(),
            self.platform.build_dir.as_posix(),
            self.platform.dist_dir.as_posix(),
            extra_options)

    def start(self):
        self.logger.info(f"generating image for {self.platform.name}")
        image = self.docker_client.images.build(path=self.platform.path.as_posix(),
                                                tag=f"crossinstaller-{self.platform.name}",
                                                rm=True,
                                                dockerfile=self.platform.dockerfile.as_posix())
        self.logger.info(f"image {self.platform.name} generated")
        self.docker_run(image[0])

    def docker_run(self, image):
        if self.stopped:
            self.logger.info("docker run canceled")
            self.cleanup()
            return
        self.logger.info(f"running image {image.tags[0]}")
        self.container = self.docker_client.containers.run(image.tags[0],
                                                           command=self.command,
                                                           detach=True,
                                                           volumes={str(Path.cwd()): {"bind": "/src",
                                                                                      "mode": "rw"}})
        self.logger.info(f"container id: {self.container.id}")
        for log in self.container.attach(stdout=True, stderr=True, stream=True, logs=True):
            self.logger.debug(str(log, encoding="utf-8"))

        exit_status = self.container.wait()['StatusCode']
        self.logger.info(f"container finished with exit status {exit_status}")
        self.cleanup()
        return self.container

    def stop(self):
        if self.container:
            self.container.stop()
        self.stopped = True

    def cleanup(self):
        if not self.keep_build:
            try:
                shutil.rmtree(str(self.platform.build_dir))
            except Exception as e:
                self.logger.error(f"could not remove build directory: {e}")
        self.finished = True

    def is_finished(self):
        return self.finished
