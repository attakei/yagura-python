"""Setup module
"""
import re
from pathlib import Path

from setuptools import find_packages, setup


def fetch_version_string(target: Path) -> str:
    line_re = re.compile(r"__version__ = '(.*?)'", re.S)
    return line_re.search(target.open().read()).group(1)


here = Path(__file__).parent

with (here / 'README.rst').open(encoding='utf-8') as f:
    long_description = f.read()

install_requires = []
with (here / 'requirements.txt').open(encoding='utf-8') as f:
    install_requires = [req.strip() for req in f.readlines() if req != '\n']


setup(
    name='yagura',
    version=fetch_version_string(here / 'yagura' / '__init__.py'),
    description='Simple website monitoring kit',
    long_description=long_description,
    url='https://gitlab.com/attakei/yagura',
    author='attakei',
    author_email='attakei@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # TODO: add after
    # keywords='django',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    extras_require={
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yagura=yagura.cli:main',
        ]
    }
)
