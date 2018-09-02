"""Yagura CLI toole endpoint
"""
import argparse
import sys

from yagura import __version__ as yagura_version

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


def version(args):
    """Display cli version
    """
    sys.stdout.write(f"Yagura-CLI version is {yagura_version}")


parser_version = subparsers.add_parser('version', help='display version')
parser_version.set_defaults(handler=version)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    if hasattr(args, 'handler'):
        return args.handler(args)
    else:
        parser.print_help()
