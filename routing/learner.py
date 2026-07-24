import random
from typing import List, Dict
from .route import Route, RouteStep

class RouteLearner:
    def __init__(self):
        self._routes: Dict[str, Route] = {}
        
    def add_route(self, route: Route):
        self._routes[route.signature] = route
        
    def get_best_route(self, required_capabilities: List[str]) -> Route:
        # MVP: just return a route that covers all, or random
        return random.choice(list(self._routes.values())) if self._routes else None
