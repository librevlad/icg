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
