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
