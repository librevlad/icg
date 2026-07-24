import subprocess
import json
from typing import Any
from nodes.base import Node
from contracts.contract import Contract
from workspace.workspace import Workspace

class GeminiCLINode(Node):
    """
    Executes reasoning and coding capabilities using a generic Gemini CLI.
    Assumes the user has a `gemini` command available in their environment.
    """
    def __init__(self, cli_command: str = "gemini"):
        self.cli_command = cli_command

    def run(self, capability: str, contract: Contract, workspace: Workspace) -> Any:
        # Build the prompt based on the contract
        prompt = self._build_prompt(capability, contract)
        
        # We pass the prompt to the CLI. 
        # Depending on the specific CLI, it might take a --prompt flag or read from stdin.
        # For this MVP, we assume a generic usage: `gemini "prompt"`
        cmd = [self.cli_command, prompt]
        
        result = subprocess.run(
            cmd,
            cwd=workspace.root_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Gemini CLI failed (code {result.returncode}): {result.stderr}")

        return {
            "capability": capability,
            "output": result.stdout.strip()
        }
        
    def _build_prompt(self, capability: str, contract: Contract) -> str:
        prompt = f"Capability Requested: {capability}\n"
        prompt += f"Task: {contract.task_description}\n"
        if contract.constraints:
            prompt += f"Constraints: {', '.join(contract.constraints)}\n"
        if contract.inputs:
            prompt += f"Inputs: {json.dumps(contract.inputs)}\n"
        prompt += "Please provide the result requested."
        return prompt
