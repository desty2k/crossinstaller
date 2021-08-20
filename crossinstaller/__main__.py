import sys
import logging
import argparse

from crossinstaller import __version__, crosscompile


def _compile(args):
    crosscompile(args.script[0], args.directory, keep_build=args.keep_build)


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

    # find and dump module to JSON
    cparser = subparsers.add_parser(
        'build',
        aliases=['b'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Generate executables',
        description="Generate executables"
    )
    cparser.add_argument('script', nargs=1, metavar='SCRIPT',
                         help='Path to script')
    cparser.add_argument('-D', '--directory', metavar='DIRECTORY',
                         help='custom source directory, default is script parent directory')
    cparser.add_argument('-K', '--keep-build', action="store_true",
                         help='Copy build directory after creating executable')
    cparser.set_defaults(func=_compile)

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
