import time
from typing import Dict, List, Any
from contracts.contract import Contract
from workspace.workspace import Workspace
from nodes.base import Node
from memory.history import History
from memory.metrics import Metrics

class ICGGraph:
    """
    ICGGraph is the Kernel of the Operating System for Distributed Intelligence.
    It manages capabilities, delegates execution to Nodes, and records history.
    """
    def __init__(self, workspace: Workspace, db_path: str = "icg_memory.db"):
        self.workspace = workspace
        self.history = History(db_path)
        self.metrics = Metrics(db_path)
        self._capabilities: Dict[str, List[Node]] = {}

    def register_node(self, node: Node, capabilities: List[str]):
        """Registers an executor (Node) as a provider for specific capabilities."""
        for cap in capabilities:
            if cap not in self._capabilities:
                self._capabilities[cap] = []
            self._capabilities[cap].append(node)

    def request(self, capability: str, contract: Contract) -> Any:
        """
        Requests execution of a specific capability for a contract.
        """
        nodes = self._capabilities.get(capability, [])
        if not nodes:
            raise ValueError(f"No node available for capability: {capability}")
        
        # MVP: Select the first available node
        chosen_node = nodes[0]
        node_name = chosen_node.__class__.__name__
        
        # Record attempt start
        record_id = self.history.log_start(contract.id, capability, node_name)
        start_time = time.time()
        
        try:
            result = chosen_node.run(capability, contract, self.workspace)
            duration = time.time() - start_time
            
            # Extract cost and tokens if node provided them
            cost = 0.0
            tokens = 0
            if isinstance(result, dict):
                cost = result.get("cost", 0.0)
                tokens = result.get("tokens", 0)
                
            self.history.log_success(record_id, cost=cost, tokens=tokens)
            self.metrics.update_metrics(node_name, capability, True, duration, cost, tokens)
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.history.log_failure(record_id, str(e))
            self.metrics.update_metrics(node_name, capability, False, duration, 0.0, 0)
            raise

    def execute(self, contract: Contract) -> Dict[str, Any]:
        """
        Executes a full contract by requesting all required capabilities.
        In the MVP, we assume capabilities are executed sequentially.
        """
        results = {}
        for cap in contract.requires:
            results[cap] = self.request(cap, contract)
        return results
