import pytest
from policy.priority import PriorityPolicy
from executors.bash import BashExecutor
from core.types import ExecutionContext

def test_priority_policy():
    p = PriorityPolicy()
    e1 = BashExecutor()
    e2 = BashExecutor()
    assert p.select("execution", [e1, e2], ExecutionContext()) == e1
