from .planner import Planner
from contracts.contract import Contract
from .execution_graph import ExecutionGraph
from .execution_node import ExecutionNode
from core.types import ExecutionNodeStatus

class SimplePlanner(Planner):
    def plan(self, contract: Contract) -> ExecutionGraph:
        graph = ExecutionGraph()
        prev_id = None
        for req in contract.requires:
            node_id = f"{contract.id}-{req}"
            node = ExecutionNode(
                id=node_id,
                capability=req,
                status=ExecutionNodeStatus.PENDING
            )
            graph.add_node(node)
            if prev_id:
                graph.add_dependency(node_id, prev_id)
            prev_id = node_id
        return graph
