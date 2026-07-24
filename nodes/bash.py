import subprocess
from typing import Any
from nodes.base import Node
from contracts.contract import Contract
from workspace.workspace import Workspace

class BashNode(Node):
    """
    Executes raw shell commands.
    It expects the contract to contain the command to run in its inputs.
    """
    def run(self, capability: str, contract: Contract, workspace: Workspace) -> Any:
        if capability != "execution":
            raise ValueError(f"BashNode does not support capability: {capability}")
            
        cmd = contract.inputs.get("command")
        if not cmd:
            raise ValueError("BashNode requires a 'command' input in the contract.")

        result = subprocess.run(
            cmd,
            shell=True,
            cwd=workspace.root_path,
            capture_output=True,
            text=True
        )

        output = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

        if result.returncode != 0:
            raise RuntimeError(f"Bash execution failed (code {result.returncode}): {result.stderr}")

        return output
