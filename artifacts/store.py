from typing import Dict, Any

class ArtifactStore:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        
    def save(self, key: str, data: Any):
        self._store[key] = data
        
    def load(self, key: str) -> Any:
        return self._store.get(key)
