import os
import shutil

files = {
    "tests/test_contract.py": """\
import pytest
from contracts.contract import Contract
from core.types import ContractStatus

def test_contract_validation():
    c = Contract(id="1", task_description="test", requires=["exec"])
    assert c.validate()
    c2 = Contract(id="", task_description="", requires=[])
    assert not c2.validate()

def test_contract_status_transitions():
    c = Contract(id="1", task_description="t", requires=["e"])
    assert c.status == ContractStatus.CREATED
    c.set_status(ContractStatus.RUNNING)
    assert c.status == ContractStatus.RUNNING
    c.set_status(ContractStatus.COMPLETED)
    assert c.status == ContractStatus.COMPLETED
""",
    "tests/test_graph.py": """\
import pytest
from core.graph import CapabilityGraph
from executors.bash import BashExecutor

def test_graph_registration():
    g = CapabilityGraph()
    e = BashExecutor()
    g.register_executor(e)
    assert "execution" in g.capabilities()
    assert g.has_capability("execution")
    assert e in g.resolve("execution")
    g.unregister(e)
    assert not g.has_capability("execution")
""",
    "tests/test_engine.py": """\
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
""",
    "tests/test_executor.py": """\
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
""",
    "tests/test_workspace.py": """\
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
""",
    "tests/test_policy.py": """\
import pytest
from policy.priority import PriorityPolicy
from executors.bash import BashExecutor
from core.types import ExecutionContext

def test_priority_policy():
    p = PriorityPolicy()
    e1 = BashExecutor()
    e2 = BashExecutor()
    assert p.select("execution", [e1, e2], ExecutionContext()) == e1
""",
    "tests/test_planner.py": """\
import pytest
from planning.simple_planner import SimplePlanner
from contracts.contract import Contract

def test_simple_planner():
    p = SimplePlanner()
    c = Contract(id="1", task_description="t", requires=["cap1", "cap2"])
    graph = p.plan(c)
    assert len(graph.nodes) == 2
    roots = graph.roots()
    assert len(roots) == 1
    assert roots[0].capability == "cap1"
""",
    "tests/test_dag.py": """\
import pytest
from planning.execution_graph import ExecutionGraph
from planning.execution_node import ExecutionNode

def test_execution_graph_cycle():
    g = ExecutionGraph()
    n1 = ExecutionNode(id="1", capability="c1")
    n2 = ExecutionNode(id="2", capability="c2")
    g.add_node(n1)
    g.add_node(n2)
    g.add_dependency("1", "2")
    g.add_dependency("2", "1")
    with pytest.raises(ValueError):
        g.validate()
""",
    "tests/test_scheduler.py": """\
import pytest
from scheduler.scheduler import Scheduler
from planning.execution_graph import ExecutionGraph
from planning.execution_node import ExecutionNode
from core.types import ExecutionNodeStatus

def test_scheduler():
    s = Scheduler()
    g = ExecutionGraph()
    n1 = ExecutionNode(id="1", capability="c1")
    n2 = ExecutionNode(id="2", capability="c2")
    g.add_node(n1)
    g.add_node(n2)
    g.add_dependency("2", "1")
    
    ready = s.next(g)
    assert len(ready) == 1
    assert ready[0].id == "1"
    
    n1.status = ExecutionNodeStatus.COMPLETED
    ready2 = s.next(g)
    assert len(ready2) == 1
    assert ready2[0].id == "2"
""",
    "tests/test_events.py": """\
import pytest
from events.event import Event, EventType
from events.bus import EventBus

def test_event_bus():
    bus = EventBus()
    received = []
    def handler(e):
        received.append(e)
    
    bus.subscribe(EventType.CONTRACT_CREATED, handler)
    bus.publish(Event(type=EventType.CONTRACT_CREATED))
    bus.publish(Event(type=EventType.CONTRACT_STARTED))
    
    assert len(received) == 1
    assert received[0].type == EventType.CONTRACT_CREATED
""",
    "tests/test_memory.py": """\
import pytest
from memory.memory import Memory
from memory.experience import Experience
import os

def test_memory():
    m = Memory(db_path="test_icg_memory.db")
    e = Experience(capability="cap1", executor_name="ex1", success=True, duration=1.0)
    m.append(e)
    q = m.query(capability="cap1")
    assert len(q) == 1
    
    stats = m.knowledge.get_stats("cap1", "ex1")
    assert stats["success_rate"] == 1.0
    if os.path.exists("test_icg_memory.db"):
        os.remove("test_icg_memory.db")
""",
    "tests/test_routing.py": """\
import pytest
from routing.route import Route, RouteStep
from routing.learner import RouteLearner

def test_routing():
    learner = RouteLearner()
    r = Route(id="1", steps=[RouteStep("cap1", "ex1")])
    learner.add_route(r)
    best = learner.get_best_route(["cap1"])
    assert best == r
"""
}

base_dir = "c:/icg"
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Cleanup
if os.path.exists(os.path.join(base_dir, "test_kernel.py")):
    os.remove(os.path.join(base_dir, "test_kernel.py"))
if os.path.exists(os.path.join(base_dir, "nodes")):
    shutil.rmtree(os.path.join(base_dir, "nodes"))

print("Tests created and legacy code cleaned up.")
