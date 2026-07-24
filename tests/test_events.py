import pytest
from events.event import Event, EventType
from events.bus import EventBus

def test_event_bus():
    bus = EventBus()
    received = []
    def handler(e):
        received.append(e)
    
    bus.subscribe(EventType.CONTRACT_CREATED, handler)
    bus.publish(Event(type=EventType.CONTRACT_CREATED))
    bus.publish(Event(type=EventType.CONTRACT_STARTED))
    
    assert len(received) == 1
    assert received[0].type == EventType.CONTRACT_CREATED
