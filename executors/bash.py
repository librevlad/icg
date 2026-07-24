import subprocess
import time
from typing import List
from executors.base import Executor
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult

class BashExecutor(Executor):
    def capabilities(self) -> List[str]:
        return ["execution"]

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start_time = time.time()
        command = contract.inputs.get("command", "")
        if not command:
            return ExecutionResult(success=False, stderr="No command provided in inputs")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=workspace.root(),
                capture_output=True,
                text=True
            )
            return ExecutionResult(
                success=(result.returncode == 0),
                stdout=result.stdout,
                stderr=result.stderr,
                error_code=str(result.returncode),
                duration=time.time() - start_time
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                stderr=str(e),
                duration=time.time() - start_time
            )
