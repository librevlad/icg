import subprocess
import time
from typing import List
from executors.base import Executor
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult

class PytestExecutor(Executor):
    def capabilities(self) -> List[str]:
        return ["verification", "testing"]

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start_time = time.time()
        try:
            result = subprocess.run(
                "python -m pytest",
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
