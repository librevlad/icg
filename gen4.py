import os
import shutil

files = {
    "cli/commands/__init__.py": "",
    
    "cli/main.py": """\
import argparse
import sys
from cli.commands import run, info, discover

def main():
    parser = argparse.ArgumentParser(description="ICG CLI - Internet Capability Graph")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run.setup_parser(subparsers)
    info.setup_parser(subparsers)
    discover.setup_parser(subparsers)
    
    args = parser.parse_args()
    
    if args.command == "run":
        sys.exit(run.execute(args))
    elif args.command in ("capabilities", "providers"):
        sys.exit(info.execute(args))
    elif args.command == "discover":
        sys.exit(discover.execute(args))

if __name__ == "__main__":
    main()
""",
    
    "cli/commands/run.py": """\
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
""",
    
    "cli/commands/info.py": """\
from providers.registry import CapabilityRegistry
from discovery.discovery import LocalDiscoveryService

def setup_parser(subparsers):
    subparsers.add_parser("capabilities", help="List all available capabilities")
    subparsers.add_parser("providers", help="List all loaded providers")

def execute(args) -> int:
    registry = CapabilityRegistry()
    discovery = LocalDiscoveryService(registry)
    discovery.discover()
    
    if args.command == "capabilities":
        caps = set()
        for p in registry.get_all():
            caps.update(p.capabilities())
        print("Available Capabilities:")
        for c in sorted(caps):
            print(f" - {c}")
            
    elif args.command == "providers":
        print("Loaded Providers:")
        for p in registry.get_all():
            print(f" - {p.manifest.id} (v{p.manifest.version})")
            
    return 0
""",
    
    "cli/commands/discover.py": """\
from providers.registry import CapabilityRegistry
from discovery.discovery import LocalDiscoveryService

def setup_parser(subparsers):
    p = subparsers.add_parser("discover", help="Scan and discover providers")
    p.add_argument("--path", default="./providers", help="Path to scan")

def execute(args) -> int:
    registry = CapabilityRegistry()
    discovery = LocalDiscoveryService(registry, search_path=args.path)
    providers = discovery.discover()
    print(f"Discovered {len(providers)} providers.")
    for p in providers:
        print(f" - {p.manifest.id}: {p.capabilities()}")
    return 0
""",
    
    "discovery/discovery.py": """\
import os
import yaml
from typing import List
from providers.registry import CapabilityRegistry
from providers.provider import Provider
from providers.manifest import ProviderManifest
from executors.base import Executor
from core.types import ExecutionResult

class DynamicExecutor(Executor):
    def __init__(self, caps):
        self._caps = caps
    def capabilities(self):
        return self._caps
    def run(self, contract, workspace):
        return ExecutionResult(success=True, stdout="Dynamic executed")

class DynamicProvider(Provider):
    def __init__(self, manifest: ProviderManifest):
        self.manifest = manifest
    def capabilities(self):
        return self.manifest.capabilities
    def get_executors(self) -> List[Executor]:
        return [DynamicExecutor(self.manifest.capabilities)]

class LocalDiscoveryService:
    def __init__(self, registry: CapabilityRegistry, search_path: str = "./providers"):
        self.registry = registry
        self.search_path = search_path
        
    def discover(self) -> List[Provider]:
        discovered = []
        if not os.path.exists(self.search_path):
            return discovered
            
        for root, _, files in os.walk(self.search_path):
            for file in files:
                if file == "manifest.yaml":
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r') as f:
                            data = yaml.safe_load(f)
                        manifest = ProviderManifest(
                            id=data.get('id', 'unknown'),
                            version=str(data.get('version', '1.0')),
                            capabilities=data.get('capabilities', [])
                        )
                        provider = DynamicProvider(manifest)
                        self.registry.register(manifest.id, provider)
                        discovered.append(provider)
                    except Exception:
                        pass
        return discovered
""",
    
    "tests/test_discovery.py": """\
import pytest
import os
import shutil
from discovery.discovery import LocalDiscoveryService
from providers.registry import CapabilityRegistry

def test_local_discovery():
    os.makedirs("test_providers/my_prov", exist_ok=True)
    with open("test_providers/my_prov/manifest.yaml", "w") as f:
        f.write("id: my_prov\\nversion: '1.0'\\ncapabilities: [\\"test_cap\\"]")
        
    reg = CapabilityRegistry()
    disc = LocalDiscoveryService(reg, "test_providers")
    provs = disc.discover()
    
    assert len(provs) == 1
    assert "test_cap" in provs[0].capabilities()
    assert len(reg.get_all()) == 1
    
    shutil.rmtree("test_providers")
""",

    "tests/test_cli.py": """\
import pytest
from cli.commands import info, discover

class DummyArgs:
    def __init__(self, command, path):
        self.command = command
        self.path = path

def test_cli_info():
    args = DummyArgs("capabilities", "./empty_prov")
    assert info.execute(args) == 0

def test_cli_discover():
    args = DummyArgs("discover", "./empty_prov")
    assert discover.execute(args) == 0
"""
}

base_dir = "c:/icg"
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Phase 8 files created.")
