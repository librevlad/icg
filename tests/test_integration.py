import pytest
import os
from contracts.contract import Contract
from core.engine import ExecutionEngine
from core.graph import CapabilityGraph
from policy.priority import PriorityPolicy
from planning.simple_planner import SimplePlanner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace
from executors.bash import BashExecutor

def test_engine_execution():
    workspace_path = "./test_ws"
    ws = Workspace(workspace_path)
    
    graph = CapabilityGraph()
    graph.register_executor(BashExecutor())
    
    engine = ExecutionEngine(
        graph=graph,
        policy=PriorityPolicy(),
        planner=SimplePlanner(),
        scheduler=Scheduler(),
        workspace=ws
    )
    
    contract = Contract(
        id="test-1",
        task_description="echo test",
        requires=["execution"],
        inputs={"command": "echo hello"}
    )
    
    result = engine.execute(contract)
    assert result.success
    assert "hello" in result.stdout
