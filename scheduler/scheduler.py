from typing import List
from planning.execution_graph import ExecutionGraph
from planning.execution_node import ExecutionNode

class Scheduler:
    def next(self, graph: ExecutionGraph) -> List[ExecutionNode]:
        return graph.ready_nodes()
