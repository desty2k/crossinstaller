# Changelog

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
