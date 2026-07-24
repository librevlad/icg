import os

files = {
    "setup.py": """\
from setuptools import setup, find_packages

setup(
    name="icg",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "icg = cli.main:main",
        ]
    },
    install_requires=[
        "PyYAML",
    ],
)
""",
    
    "executors/gemini_api.py": """\
import os
import json
import urllib.request
import urllib.error
import time
from typing import List
from executors.base import Executor
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult

class GeminiAPIExecutor(Executor):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def capabilities(self) -> List[str]:
        return ["reasoning", "coding"]

    def _build_prompt(self, contract: Contract) -> str:
        prompt = f"Task: {contract.task_description}\\n"
        if contract.inputs:
            prompt += f"Inputs: {json.dumps(contract.inputs)}\\n"
        if contract.constraints:
            prompt += f"Constraints: {json.dumps(contract.constraints)}\\n"
        return prompt

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        if not self.api_key:
            return ExecutionResult(success=False, stderr="GEMINI_API_KEY environment variable is not set")
            
        start_time = time.time()
        prompt = self._build_prompt(contract)
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result_json = json.loads(response.read().decode('utf-8'))
                
                try:
                    text = result_json['candidates'][0]['content']['parts'][0]['text']
                    return ExecutionResult(
                        success=True,
                        stdout=text,
                        duration=time.time() - start_time
                    )
                except (KeyError, IndexError):
                    return ExecutionResult(
                        success=False,
                        stderr=f"Unexpected API response structure: {result_json}",
                        duration=time.time() - start_time
                    )
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return ExecutionResult(
                success=False,
                stderr=f"HTTP Error {e.code}: {error_body}",
                duration=time.time() - start_time
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                stderr=str(e),
                duration=time.time() - start_time
            )
""",

    "cli/commands/run.py": """\
import os
from contracts.serializer import ContractSerializer
from core.engine import ExecutionEngine
from core.graph import CapabilityGraph
from policy.priority import PriorityPolicy
from planning.simple_planner import SimplePlanner
from scheduler.scheduler import Scheduler
from workspace.workspace import Workspace
from executors.bash import BashExecutor
from executors.gemini_api import GeminiAPIExecutor
from discovery.discovery import LocalDiscoveryService
from providers.registry import CapabilityRegistry

def setup_parser(subparsers):
    p = subparsers.add_parser("run", help="Run a contract")
    p.add_argument("contract_file", help="Path to contract JSON/YAML")
    p.add_argument("--workspace", default="./workspace", help="Workspace path")

def execute(args) -> int:
    with open(args.contract_file, 'r') as f:
        content = f.read()
        if args.contract_file.endswith('.json'):
            contract = ContractSerializer.from_json(content)
        else:
            contract = ContractSerializer.from_yaml(content)
            
    workspace = Workspace(args.workspace)
    graph = CapabilityGraph()
    registry = CapabilityRegistry()
    
    discovery = LocalDiscoveryService(registry)
    providers = discovery.discover()
    for p in providers:
        for ex in p.get_executors():
            graph.register_executor(ex)
            
    graph.register_executor(BashExecutor())
    graph.register_executor(GeminiAPIExecutor())
    
    engine = ExecutionEngine(
        graph=graph,
        policy=PriorityPolicy(),
        planner=SimplePlanner(),
        scheduler=Scheduler(),
        workspace=workspace
    )
    
    result = engine.execute(contract)
    print("Success:" if result.success else "Failed:", result.stderr or result.stdout)
    return 0 if result.success else 1
""",

    "examples/hello_world.yaml": """\
id: "example-hello"
task_description: "Print a greeting message"
requires: 
  - execution
inputs:
  command: "echo 'Hello World from ICG!'"
""",

    "examples/write_code.yaml": """\
id: "example-write-code"
task_description: "Write a simple Python script to calculate Fibonacci sequence and print the 10th number."
requires:
  - coding
constraints:
  language: "python"
  output_format: "Provide only the python code block, nothing else."
"""
}

base_dir = "c:/icg"
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Phase 9 files created.")
