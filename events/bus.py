from typing import Callable, Dict, List
from .event import Event, EventType

class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        
    def unsubscribe(self, event_type: EventType, handler: Callable):
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            
    def publish(self, event: Event):
        for handler in self._subscribers.get(event.type, []):
            handler(event)
