import argparse
import sys
from contracts.contract import Contract
from contracts.serializer import ContractSerializer
from core.engine import ExecutionEngine
from core.graph import CapabilityGraph
from policy.priority import PriorityPolicy
from planning.simple_planner import SimplePlanner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace
from executors.bash import BashExecutor

def main():
    parser = argparse.ArgumentParser(description="ICG CLI")
    parser.add_argument("contract_file", help="Path to contract JSON/YAML")
    parser.add_argument("--workspace", default="./workspace", help="Workspace path")
    args = parser.parse_args()
    
    with open(args.contract_file, 'r') as f:
        content = f.read()
        if args.contract_file.endswith('.json'):
            contract = ContractSerializer.from_json(content)
        else:
            contract = ContractSerializer.from_yaml(content)
            
    workspace = Workspace(args.workspace)
    graph = CapabilityGraph()
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
    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()
