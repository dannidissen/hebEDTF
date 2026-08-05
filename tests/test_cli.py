"""Tests for hebedtf.cli module."""

import io
import json

from hebedtf.cli import main


def test_cli_basic(capsys):
    ret = main(['כ"ג בתשרי תשפ"ד'])
    assert ret == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "2023-10-08"


def test_cli_json(capsys):
    ret = main(['--json', 'בערך תש"ח'])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["input"] == 'בערך תש"ח'
    assert data["edtf"] == "1947-09-15/1948-10-03~"


def test_cli_no_args_returns_help(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    ret = main([])
    assert ret == 1
