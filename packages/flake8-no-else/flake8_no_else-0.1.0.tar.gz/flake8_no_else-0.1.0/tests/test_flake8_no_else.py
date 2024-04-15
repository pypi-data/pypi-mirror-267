from flake8_no_else import Plugin
from typing import Set
from ast import parse
import pytest


def _results(s: str) -> Set[str]: 
    tree = parse(s)
    plugin = Plugin(tree=tree)
    return {f'{line}:{col} {msg}' for line, col, msg, _ in plugin.run()}


def test_():
    assert _results('') == set()


@pytest.mark.parametrize('path,expected', [
    ('./tests/masters/elif.py', {'2:4 FNE101 ELIF found'}), 
    ('./tests/masters/else.py', {'2:4 FNE100 ELSE found'}), 
    ('./tests/masters/ternary.py', {'2:11 FNE102 ternary ELSE found'}), 
])
def test_fails_for_else(path, expected):
    with open(path, 'r') as file: 
        func = file.read()
    ret = _results(func)
    assert ret == expected
