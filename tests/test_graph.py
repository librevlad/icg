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
