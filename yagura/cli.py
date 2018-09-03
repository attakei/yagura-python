"""Yagura CLI toole endpoint
"""
import argparse
import shutil
import sys
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from yagura import __version__ as yagura_version

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


def version(args):
    """Display cli version
    """
    sys.stdout.write(f"Yagura-CLI version is {yagura_version}")


parser_version = subparsers.add_parser('version', help='display version')
parser_version.set_defaults(handler=version)


def _render_resource(from_: Path, to_: Path, context: dict):
    with from_.open() as src:
        with to_.open('w') as dest:
            for l in src:
                if '{' in l and '}' in l:
                    dest.write(l.format(**context))
                else:
                    dest.write(l)


def init(args):
    """Create yagura based application
    """
    proj_dir = Path(args.proj_dir)
    proj_module_dir = proj_dir / str(proj_dir.name)
    if proj_dir.exists():
        sys.stderr.write('Application is already exists')
        return False
    proj_module_dir.mkdir(parents=True)
    proj_template_dir = Path(__file__).parent / 'project_template'
    # Copy resources
    shutil.copyfile(proj_template_dir / 'requirements.txt', proj_dir / 'requirements.txt')
    shutil.copyfile(proj_template_dir / 'myproj/__init__.py', proj_module_dir / '__init__.py')
    shutil.copyfile(proj_template_dir / 'myproj/urls.py', proj_module_dir / 'urls.py')
    # Write resources with variables
    context = {
        'project_name': proj_dir.name,
        'secret_key': get_random_secret_key(),
    }
    _render_resource(proj_template_dir / 'manage.py', proj_dir / 'manage.py', context)
    _render_resource(proj_template_dir / 'myproj/settings.py', proj_module_dir / 'settings.py', context)
    

parser_init = subparsers.add_parser('init', help=init.__doc__)
parser_init.add_argument('proj_dir')
parser_init.set_defaults(handler=init)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    if hasattr(args, 'handler'):
        return args.handler(args)
    else:
        parser.print_help()
