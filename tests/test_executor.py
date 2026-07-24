import pytest
from executors.bash import BashExecutor
from contracts.contract import Contract
from workspace.workspace import Workspace

def test_bash_executor():
    ws = Workspace("./test_ws_bash")
    e = BashExecutor()
    c = Contract(id="1", task_description="test", requires=["execution"], inputs={"command": "echo hello"})
    res = e.run(c, ws)
    assert res.success
    assert "hello" in res.stdout
