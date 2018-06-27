"""Setup module
"""
import sys
from codecs import open
from os import path

from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))
sys.path.append(here)

import yagura  # noqa: flake8


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = []
with open('requirements.txt') as fp:
    install_requires = [req.strip() for req in fp.readlines() if req != '\n']


setup(
    name='yagura',
    version=yagura.__version__,
    description='Simple website monitoring kit',
    long_description=long_description,
    url='https://gitlab.com/attakei/yagura',
    author='attakei',
    author_email='attakei@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
    ],
    # TODO: add after
    # keywords='django',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    extras_require={
    },
    include_package_data=True,
)
