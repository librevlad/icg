from typing import Dict, List
from .execution_node import ExecutionNode
from core.types import ExecutionNodeStatus

class ExecutionGraph:
    def __init__(self):
        self._nodes: Dict[str, ExecutionNode] = {}

    def add_node(self, node: ExecutionNode):
        self._nodes[node.id] = node

    def add_dependency(self, node_id: str, depends_on: str):
        if node_id in self._nodes and depends_on in self._nodes:
            if depends_on not in self._nodes[node_id].dependencies:
                self._nodes[node_id].dependencies.append(depends_on)

    def get_node(self, node_id: str) -> ExecutionNode:
        return self._nodes.get(node_id)

    def roots(self) -> List[ExecutionNode]:
        return [node for node in self._nodes.values() if not node.dependencies]

    def ready_nodes(self) -> List[ExecutionNode]:
        ready = []
        for node in self._nodes.values():
            if node.status == ExecutionNodeStatus.PENDING:
                all_deps_completed = all(
                    self._nodes[dep].status == ExecutionNodeStatus.COMPLETED
                    for dep in node.dependencies
                )
                if all_deps_completed:
                    ready.append(node)
        return ready

    def validate(self) -> bool:
        visited = set()
        path = set()

        def visit(node_id: str):
            if node_id in path:
                raise ValueError("Cycle detected in ExecutionGraph")
            if node_id in visited:
                return
            path.add(node_id)
            for dep in self._nodes[node_id].dependencies:
                visit(dep)
            path.remove(node_id)
            visited.add(node_id)

        for n_id in self._nodes:
            visit(n_id)
        return True

    def is_complete(self) -> bool:
        return all(
            node.status in (ExecutionNodeStatus.COMPLETED, ExecutionNodeStatus.FAILED)
            for node in self._nodes.values()
        )

    @property
    def nodes(self) -> List[ExecutionNode]:
        return list(self._nodes.values())
