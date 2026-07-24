import pytest
from core.engine import ExecutionEngine
from core.graph import CapabilityGraph
from policy.priority import PriorityPolicy
from planning.simple_planner import SimplePlanner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace
from executors.bash import BashExecutor
from contracts.contract import Contract

def test_engine_end_to_end():
    ws = Workspace("./test_ws_engine")
    g = CapabilityGraph()
    g.register_executor(BashExecutor())
    engine = ExecutionEngine(g, PriorityPolicy(), SimplePlanner(), Scheduler(), ws)
    
    c = Contract(id="1", task_description="test", requires=["execution"], inputs={"command": "echo 1"})
    res = engine.execute(c)
    assert res.success
    assert "1" in res.stdout
