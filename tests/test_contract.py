import pytest
from contracts.contract import Contract
from core.types import ContractStatus

def test_contract_validation():
    c = Contract(id="1", task_description="test", requires=["exec"])
    assert c.validate()
    c2 = Contract(id="", task_description="", requires=[])
    assert not c2.validate()

def test_contract_status_transitions():
    c = Contract(id="1", task_description="t", requires=["e"])
    assert c.status == ContractStatus.CREATED
    c.set_status(ContractStatus.RUNNING)
    assert c.status == ContractStatus.RUNNING
    c.set_status(ContractStatus.COMPLETED)
    assert c.status == ContractStatus.COMPLETED
