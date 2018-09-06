"""Test case for CLI endpoint behavior
"""
import contextlib
import os
import tempfile
from pathlib import Path

from yagura import __version__ as yagura_version
from yagura.cli import main


@contextlib.contextmanager
def cd(path):
    """Change current directory in context
    """
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


def test_version(capsys):
    main(['version'])
    captured = capsys.readouterr()
    assert 'Yagura-CLI version' in captured.out
    assert f"{yagura_version}" in captured.out


class InitCommandTests(object):
    def test_folder_created(self):
        tempdir = Path(tempfile.mkdtemp())
        with cd(tempdir):
            main(['init', 'testapp'])
            app_dir = tempdir / 'testapp'
            assert app_dir.exists() is True

    def test_folder_exists(self):
        tempdir = Path(tempfile.mkdtemp())
        (tempdir / 'testapp').mkdir()
        with cd(tempdir):
            result = main(['init', 'testapp'])
            assert result is False

    def test_has_files(self):
        tempdir = Path(tempfile.mkdtemp())
        with cd(tempdir):
            main(['init', 'testapp'])
            app_dir = tempdir / 'testapp'
            assert (app_dir / 'requirements.txt').exists() is True
