# Changelog

- 0.1.0:
  - Move all core function to `crossinstaller.building` module
  - Get version from `\_\_init__` not `\_\_main__`when installing
  - Remove pyarmor from Dockerfiles
  - Do not require `docker` package in `build` workflow
  - Add badges to readme
  - Require `docker` package when installing `crossisntaller`

- 0.0.5:
  - Add clear platforms option
  - Add `version` key in platform.json
  - Fix FileNotFound when removing unused files from images directory
  - Add build and deploy workflows

- 0.0.4:
  - Add `-e / --extra` for extra arguments for PyInstaller
  - Remove `build` directory when all containers exit
  - Cleanup after exception in image building process

- 0.0.3:
  - Store platforms in JSON file
  - Add `platform` arguments parser and `add`, `remove`, `list` subcommands
  - Add `Platform` model

- 0.0.2:
  - Add new general exception CrossInstallerError
  - Do not create temporary directories for each container

- 0.0.1:
  - Initial commit
