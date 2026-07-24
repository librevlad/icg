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
        task_description=f"Apply {req.capability} to {req.object.type}\nObject Data: {req.object.data}",
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
