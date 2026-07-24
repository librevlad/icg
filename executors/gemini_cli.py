import subprocess
import time
from typing import List
from executors.base import Executor
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult

class GeminiCLIExecutor(Executor):
    def __init__(self, cli_command="gemini"):
        self.cli_command = cli_command

    def capabilities(self) -> List[str]:
        return ["reasoning", "planning", "coding"]

    def _build_prompt(self, contract: Contract) -> str:
        return f"{contract.task_description}\nRequires: {contract.requires}"

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start_time = time.time()
        prompt = self._build_prompt(contract)
        
        try:
            result = subprocess.run(
                f'{self.cli_command} prompt "{prompt}"',
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
