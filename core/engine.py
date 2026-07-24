from contracts.contract import Contract
from core.types import ExecutionResult, ExecutionContext, ContractStatus, ExecutionNodeStatus
from core.graph import CapabilityGraph
from policy.base import ExecutionPolicy
from planning.planner import Planner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace

class ExecutionEngine:
    def __init__(self, graph: CapabilityGraph, policy: ExecutionPolicy, 
                 planner: Planner, scheduler: Scheduler,
                 workspace: Workspace, event_bus=None, memory=None):
        self.graph = graph
        self.policy = policy
        self.planner = planner
        self.scheduler = scheduler
        self.workspace = workspace
        self.event_bus = event_bus
        self.memory = memory

    def execute(self, contract: Contract) -> ExecutionResult:
        if not contract.validate():
            return ExecutionResult(success=False, stderr="Invalid contract")
        
        contract.set_status(ContractStatus.RUNNING)
        context = ExecutionContext(contract=contract, workspace=self.workspace, memory=self.memory)
        
        plan = self.planner.plan(contract)
        try:
            plan.validate()
        except ValueError as e:
            contract.set_status(ContractStatus.FAILED)
            return ExecutionResult(success=False, stderr=str(e))
            
        aggregated_stdout = ""
        aggregated_stderr = ""
        
        while not plan.is_complete():
            ready_nodes = self.scheduler.next(plan)
            if not ready_nodes:
                contract.set_status(ContractStatus.FAILED)
                return ExecutionResult(success=False, stderr="Stalled: No ready nodes and plan not complete")
                
            for node in ready_nodes:
                try:
                    candidates = self.graph.resolve(node.capability)
                    executor = self.policy.select(node.capability, candidates, context)
                    result = executor.run(contract, self.workspace)
                    
                    node.result = result
                    if not result.success:
                        node.status = ExecutionNodeStatus.FAILED
                        contract.set_status(ContractStatus.FAILED)
                        return result
                    
                    node.status = ExecutionNodeStatus.COMPLETED
                    aggregated_stdout += result.stdout + "\n"
                    aggregated_stderr += result.stderr + "\n"
                except Exception as e:
                    node.status = ExecutionNodeStatus.FAILED
                    contract.set_status(ContractStatus.FAILED)
                    return ExecutionResult(success=False, stderr=str(e))
                    
        contract.set_status(ContractStatus.COMPLETED)
        return ExecutionResult(success=True, stdout=aggregated_stdout, stderr=aggregated_stderr)
