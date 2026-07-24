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
