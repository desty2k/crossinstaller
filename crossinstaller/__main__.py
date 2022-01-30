import os
import sys
import logging
import argparse
from pathlib import Path

from crossinstaller import CrossInstaller
from crossinstaller.config import __version__
from crossinstaller.platform import get_default_platforms, get_platform_by_name


def _build(args):
    # check if script exists
    script_path = Path(args.script[0])
    if not script_path.exists():
        raise FileNotFoundError(f"script {script_path} not found")
    # make sure we are in the script's directory
    os.chdir(script_path.parent)

    # check if platforms are specified
    def_platforms = get_default_platforms()
    platforms = []
    if args.platform is None:
        platforms = def_platforms
    else:
        for arg_platform in args.platform:
            platform = get_platform_by_name(arg_platform)
            if platform is None:
                raise ValueError(f"unknown platform {arg_platform}, available platforms: "
                                 f"{', '.join([p.name for p in def_platforms])}")
            platforms.append(platform)

    # check if options are specified
    options = args.options if args.options is not None else ""

    builder = CrossInstaller()
    builder.add_platforms(platforms)
    builder.start(script_path, args.keep, options)
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
    parser.add_argument("-p", "--platform", action="append",
                        help="platform to build for")
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
    logging.basicConfig(format="%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
                        level=logging.NOTSET)

    parser = _parser()
    args = parser.parse_args(argv)
    logging.getLogger().setLevel(logging.getLevelName(args.log_level.upper()))
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    args.func(args)


def main_entry():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(message)s',
    )
    main(sys.argv[1:])


if __name__ == '__main__':
    main_entry()
