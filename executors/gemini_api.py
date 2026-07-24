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
        prompt = f"Task: {contract.task_description}\n"
        if contract.inputs:
            prompt += f"Inputs: {json.dumps(contract.inputs)}\n"
        if contract.constraints:
            prompt += f"Constraints: {json.dumps(contract.constraints)}\n"
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
