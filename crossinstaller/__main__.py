import sys
import logging
import argparse

from crossinstaller import __version__, build, load_platforms, add_platform, save_platforms


def _build(args):
    build(args.script[0], keep_build=args.keep_build)


def _platform_list(args):
    print("Name - Image - Extra files")
    platforms = load_platforms()
    for platform in platforms:
        print(platform.name, " - ", platform.image, " -  [", " ".join(extra for extra in platform.extra_files), "]")


def _platform_add(args):
    if args.extra_file is not None:
        extra = [arg[0] for arg in args.extra_file]
    else:
        extra = []
    add_platform(args.name[0], args.image, extra, overwrite=args.overwrite)
    print("Platform '{}' added successfully".format(args.name[0]))


def _platform_remove(args):
    platforms = load_platforms()
    platform_to_delete = None
    for platform in platforms:
        if platform.name == args.name[0]:
            platform_to_delete = platform
    if platform_to_delete is None:
        raise KeyError("platform '{}' does not exists".format(args.name[0]))
    else:
        platforms.remove(platform_to_delete)
        save_platforms(platforms)
        print("Platform '{}' removed successfully".format(args.name[0]))


def _parser():
    parser = argparse.ArgumentParser(
        prog='crossinstaller',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Multi platform installer",
        epilog='See "crossinstaller <command> -h" for more information '
               'on a specific command.'
    )

    parser.add_argument('-V', '--version', action='version', version='v{}'.format(__version__),
                        help='print version and exit')

    subparsers = parser.add_subparsers(
        title='Available commands',
        metavar=''
    )

    # building executable
    cparser = subparsers.add_parser(
        'build',
        aliases=['b'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Generate executables',
        description="Generate executables"
    )
    cparser.add_argument('script', nargs=1, metavar='SCRIPT',
                         help='Path to script')
    cparser.add_argument('-K', '--keep-build', action="store_true",
                         help='Copy build directory after creating executable')
    cparser.set_defaults(func=_build)

    # subparser for editing platforms and Docker images
    cparser = subparsers.add_parser(
        'platform',
        aliases=['p'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Manage platforms and Docker images',
        description='Manage platforms and Docker images'
    )

    platform_subparser = cparser.add_subparsers(
        title='Manage platforms and Docker images',
        metavar=''
    )

    # add new platform
    platform_cparser = platform_subparser.add_parser(
        'add',
        aliases=['a'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Add platforms',
        description='Add platforms'
    )
    platform_cparser.add_argument('name', nargs=1, metavar='NAME',
                                  help='Platform name')
    platform_cparser.add_argument('-I', '--image', metavar='IMAGE', required=True,
                                  help='path to Docker image')
    platform_cparser.add_argument('-E', '--extra-file', metavar='FILE', action='append', nargs=1,
                                  help='Extra file required by image. Can be used multiple times.')
    platform_cparser.add_argument('-O', '--overwrite', action="store_true",
                                  help='Overwrite image if already exists')
    platform_cparser.set_defaults(func=_platform_add)

    # remove platform
    platform_cparser = platform_subparser.add_parser(
        'remove',
        aliases=['r'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Remove platforms',
        description='Remove platforms'
    )
    platform_cparser.add_argument('name', nargs=1, metavar='NAME',
                                  help='Platform name')
    platform_cparser.set_defaults(func=_platform_remove)

    # print all platforms
    platform_cparser = platform_subparser.add_parser(
        'list',
        aliases=['l'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Show available platforms',
        description='Show available platforms'
    )
    platform_cparser.set_defaults(func=_platform_list)

    return parser


def main(argv):
    parser = _parser()
    args = parser.parse_args(argv)
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
