from .worker import Worker
from core.engine import ExecutionEngine
from contracts.contract import Contract
from core.types import ExecutionResult

class Runtime:
    def __init__(self, engine: ExecutionEngine):
        self.engine = engine
        
    def run(self, contract: Contract) -> ExecutionResult:
        return self.engine.execute(contract)
