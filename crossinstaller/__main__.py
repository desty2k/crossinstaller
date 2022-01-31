import os
import sys
import logging
import argparse
from pathlib import Path

from crossinstaller import CrossInstaller, Platform
from crossinstaller.config import __version__
from crossinstaller.platform import get_default_platforms, get_platform_by_name


def _build(args):
    # get script path
    script_path = Path(args.script[0]).absolute()
    # get workdir
    workdir = args.workdir
    if workdir is not None:
        workdir = Path(args.workdir).absolute()

    # check if platforms are specified
    def_platforms = get_default_platforms()
    platforms: list[Platform] = []

    # check for user defined platforms
    if args.add_platform is not None:
        for name, dockerfile_path in args.add_platform:
            if get_platform_by_name(name) is not None:
                raise ValueError(f"platform {name} already exists")
            dockerfile_path = Path(dockerfile_path)
            print(Path.cwd(), dockerfile_path)
            if not dockerfile_path.exists():
                raise FileNotFoundError(f"dockerfile '{dockerfile_path}' not found")
            platforms.append(Platform(name, dockerfile_path))

    # check for default platforms
    if args.platform is not None:
        for arg_platform in args.platform:
            platform = get_platform_by_name(arg_platform)
            if platform is None:
                raise ValueError(f"unknown platform {arg_platform}, available platforms: "
                                 f"{', '.join([p.name for p in def_platforms])}")
            platforms.append(platform)

    # check if we have any platforms
    if len(platforms) == 0:
        raise ValueError("you have to specify at least one platform")

    # check if options are specified
    options = args.options if args.options is not None else ""

    builder = CrossInstaller()
    builder.add_platforms(platforms)
    builder.start(script_path, workdir, args.keep, options)
    builder.wait()


def _parser():
    parser = argparse.ArgumentParser(
        prog="crossinstaller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Multi platform installer",
        epilog="See \"crossinstaller <command> -h\" for more information "
               "on a specific command."
    )
    parser.add_argument("script", nargs=1,
                        help="script to build")
    parser.add_argument("-w", "--workdir", action="store",
                        default=None, help="workdir to use")
    parser.add_argument("-p", "--platform", action="append",
                        help="platform to build for")
    parser.add_argument("-a", "--add-platform", action="append", nargs=2,
                        help="build for custom platform", metavar=("NAME", "DOCKERFILE_PATH"))
    parser.add_argument("-k", "--keep", "--debug", action="store_true",
                        help="keep build directory")
    parser.add_argument("-e", "--options", metavar="EXTRA_OPTIONS",
                        help="pass these extra options to \"pyinstaller\"")

    parser.add_argument("--log-level", default="WARNING",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="set log level")
    parser.add_argument("-V", "--version", action="version", version=f"v{__version__}",
                        help="print version and exit")

    parser.set_defaults(func=_build)
    return parser


def main(argv):
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("docker").setLevel(logging.WARNING)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s"))

    logger = logging.getLogger()
    logger.addHandler(handler)

    parser = _parser()
    args = parser.parse_args(argv)
    logger.setLevel(logging.getLevelName(args.log_level.upper()))
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    args.func(args)


def main_entry():
    main(sys.argv[1:])


if __name__ == '__main__':
    main_entry()
