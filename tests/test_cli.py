import pytest
from cli.commands import info, discover

class DummyArgs:
    def __init__(self, command, path):
        self.command = command
        self.path = path

def test_cli_info():
    args = DummyArgs("capabilities", "./empty_prov")
    assert info.execute(args) == 0

def test_cli_discover():
    args = DummyArgs("discover", "./empty_prov")
    assert discover.execute(args) == 0
