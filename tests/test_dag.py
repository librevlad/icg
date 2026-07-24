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
