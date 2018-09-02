"""Test case for CLI endpoint behavior
"""
from yagura import __version__ as yagura_version
from yagura.cli import main


def test_version(capsys):
    main(['version'])
    captured = capsys.readouterr()
    assert 'Yagura-CLI version' in captured.out
    assert f"{yagura_version}" in captured.out
