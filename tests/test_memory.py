import pytest
from memory.memory import Memory
from memory.experience import Experience
import os

def test_memory():
    m = Memory(db_path="test_icg_memory.db")
    e = Experience(capability="cap1", executor_name="ex1", success=True, duration=1.0)
    m.append(e)
    q = m.query(capability="cap1")
    assert len(q) == 1
    
    stats = m.knowledge.get_stats("cap1", "ex1")
    assert stats["success_rate"] == 1.0
