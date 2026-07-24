import pytest
from workspace.workspace import Workspace

def test_workspace_operations():
    ws = Workspace("./test_ws_ops")
    ws.write("test.txt", "content")
    assert ws.exists()
    assert ws.read("test.txt") == "content"
    assert "test.txt" in ws.list_files()
    ws.delete("test.txt")
    assert "test.txt" not in ws.list_files()
