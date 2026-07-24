from core.graph import CapabilityGraph

class GraphSerializer:
    @staticmethod
    def serialize(graph: CapabilityGraph) -> str:
        return str(graph.capabilities())
