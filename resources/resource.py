from dataclasses import dataclass
from typing import Dict

@dataclass
class Resource:
    id: str
    type: str
    capacity: int

class ResourceGraph:
    def __init__(self):
        self._resources: Dict[str, Resource] = {}
        
    def add(self, resource: Resource):
        self._resources[resource.id] = resource
