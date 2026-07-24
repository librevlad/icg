import os
from contracts.serializer import ContractSerializer
from core.engine import ExecutionEngine
from core.graph import CapabilityGraph
from policy.priority import PriorityPolicy
from planning.simple_planner import SimplePlanner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace
from executors.bash import BashExecutor
from discovery.discovery import LocalDiscoveryService
from providers.registry import CapabilityRegistry

def setup_parser(subparsers):
    p = subparsers.add_parser("run", help="Run a contract")
    p.add_argument("contract_file", help="Path to contract JSON/YAML")
    p.add_argument("--workspace", default="./workspace", help="Workspace path")

def execute(args) -> int:
    with open(args.contract_file, 'r') as f:
        content = f.read()
        if args.contract_file.endswith('.json'):
            contract = ContractSerializer.from_json(content)
        else:
            contract = ContractSerializer.from_yaml(content)
            
    workspace = Workspace(args.workspace)
    graph = CapabilityGraph()
    registry = CapabilityRegistry()
    
    discovery = LocalDiscoveryService(registry)
    providers = discovery.discover()
    for p in providers:
        for ex in p.get_executors():
            graph.register_executor(ex)
            
    graph.register_executor(BashExecutor())
    
    engine = ExecutionEngine(
        graph=graph,
        policy=PriorityPolicy(),
        planner=SimplePlanner(),
        scheduler=Scheduler(),
        workspace=workspace
    )
    
    result = engine.execute(contract)
    print("Success:" if result.success else "Failed:", result.stderr or result.stdout)
    return 0 if result.success else 1
