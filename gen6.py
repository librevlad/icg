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
        "fastapi",
        "uvicorn",
        "pydantic"
    ],
)
""",
    
    "api/__init__.py": "",
    
    "api/models.py": """\
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PointObject(BaseModel):
    id: str
    type: str  # e.g., "text", "image", "pdf"
    data: Any  # Base64 string, plain text, or JSON
    metadata: Dict[str, Any] = {}

class CapabilityResponse(BaseModel):
    object_type: str
    capabilities: List[str]

class ExecutionRequest(BaseModel):
    object: PointObject
    capability: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    success: bool
    new_object: Optional[PointObject] = None
    error: Optional[str] = None
""",
    
    "api/server.py": """\
from fastapi import FastAPI, HTTPException
import uuid
from typing import List

from api.models import PointObject, CapabilityResponse, ExecutionRequest, ExecutionResponse
from contracts.contract import Contract
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

app = FastAPI(title="Point Backend (ICG)", version="1.0.0")

def get_engine():
    workspace = Workspace("./workspace")
    graph = CapabilityGraph()
    registry = CapabilityRegistry()
    
    discovery = LocalDiscoveryService(registry)
    providers = discovery.discover()
    for p in providers:
        for ex in p.get_executors():
            graph.register_executor(ex)
            
    graph.register_executor(BashExecutor())
    graph.register_executor(GeminiAPIExecutor())
    
    return ExecutionEngine(
        graph=graph,
        policy=PriorityPolicy(),
        planner=SimplePlanner(),
        scheduler=Scheduler(),
        workspace=workspace
    )

@app.get("/capabilities", response_model=CapabilityResponse)
def get_capabilities(object_type: str = "any"):
    engine = get_engine()
    caps = engine.graph.capabilities()
    return CapabilityResponse(object_type=object_type, capabilities=caps)

@app.post("/execute", response_model=ExecutionResponse)
def execute_capability(req: ExecutionRequest):
    engine = get_engine()
    
    if not engine.graph.has_capability(req.capability):
        raise HTTPException(status_code=400, detail=f"Capability {req.capability} not found")
        
    contract_id = f"point-{uuid.uuid4()}"
    
    # Map Point Object to ICG Contract Inputs
    inputs = {
        "object_type": req.object.type,
        "object_data": req.object.data,
        "parameters": req.parameters or {}
    }
    
    contract = Contract(
        id=contract_id,
        task_description=f"Apply {req.capability} to {req.object.type}\\nObject Data: {req.object.data}",
        requires=[req.capability],
        inputs=inputs
    )
    
    result = engine.execute(contract)
    
    if not result.success:
        return ExecutionResponse(success=False, error=result.stderr or result.error_code or "Execution failed")
        
    # Map ICG Output back to Point Object
    new_obj = PointObject(
        id=str(uuid.uuid4()),
        type="text",
        data=result.stdout,
        metadata={"source_capability": req.capability}
    )
    
    return ExecutionResponse(success=True, new_object=new_obj)
""",
    
    "cli/commands/serve.py": """\
import uvicorn

def setup_parser(subparsers):
    p = subparsers.add_parser("serve", help="Start the ICG API server for Point clients")
    p.add_argument("--host", default="0.0.0.0", help="Host interface to bind to")
    p.add_argument("--port", type=int, default=8000, help="Port to listen on")

def execute(args) -> int:
    print(f"Starting Point Backend API on {args.host}:{args.port}...")
    uvicorn.run("api.server:app", host=args.host, port=args.port, reload=False)
    return 0
""",
    
    "cli/main.py": """\
import argparse
import sys
from cli.commands import run, info, discover, serve

def main():
    parser = argparse.ArgumentParser(description="ICG CLI - Internet Capability Graph")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run.setup_parser(subparsers)
    info.setup_parser(subparsers)
    discover.setup_parser(subparsers)
    serve.setup_parser(subparsers)
    
    args = parser.parse_args()
    
    if args.command == "run":
        sys.exit(run.execute(args))
    elif args.command in ("capabilities", "providers"):
        sys.exit(info.execute(args))
    elif args.command == "discover":
        sys.exit(discover.execute(args))
    elif args.command == "serve":
        sys.exit(serve.execute(args))

if __name__ == "__main__":
    main()
"""
}

base_dir = "c:/icg"
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Phase 10 files created.")
