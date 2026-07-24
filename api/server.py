from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from executors.point_builtins import TextAnalyzerExecutor, TransformExecutor, SummarizeExecutor
from discovery.discovery import LocalDiscoveryService
from providers.registry import CapabilityRegistry

app = FastAPI(
    title="Point Backend (ICG)",
    version="1.0.0",
    description="Internet Capability Graph — Object Runtime backend for Point"
)

# Allow Point clients from any origin (Android, browser, desktop)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton engine — built once at startup
_engine = None

def get_engine() -> ExecutionEngine:
    global _engine
    if _engine is not None:
        return _engine

    workspace = Workspace("./workspace")
    graph = CapabilityGraph()
    registry = CapabilityRegistry()

    discovery = LocalDiscoveryService(registry)
    providers = discovery.discover()
    for p in providers:
        for ex in p.get_executors():
            graph.register_executor(ex)

    # Core executors
    graph.register_executor(BashExecutor())
    graph.register_executor(GeminiAPIExecutor())

    # Point built-in executors (no API key needed)
    graph.register_executor(TextAnalyzerExecutor())
    graph.register_executor(TransformExecutor())
    graph.register_executor(SummarizeExecutor())

    _engine = ExecutionEngine(
        graph=graph,
        policy=PriorityPolicy(),
        planner=SimplePlanner(),
        scheduler=Scheduler(),
        workspace=workspace,
    )
    return _engine


@app.get("/")
def root():
    return {
        "name": "Point Backend (ICG)",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/capabilities", response_model=CapabilityResponse)
def get_capabilities(object_type: str = "any"):
    engine = get_engine()
    caps = engine.graph.capabilities()
    return CapabilityResponse(object_type=object_type, capabilities=caps)


@app.post("/execute", response_model=ExecutionResponse)
def execute_capability(req: ExecutionRequest):
    engine = get_engine()

    if not engine.graph.has_capability(req.capability):
        raise HTTPException(status_code=400, detail=f"Capability '{req.capability}' not found")

    contract_id = f"point-{uuid.uuid4()}"

    inputs = {
        "object_type": req.object.type,
        "object_data": req.object.data,
        "parameters": req.parameters or {},
    }

    # For bash execution, map object_data as the command
    if req.capability == "execution":
        inputs["command"] = str(req.object.data)

    contract = Contract(
        id=contract_id,
        task_description=f"Apply '{req.capability}' to object of type '{req.object.type}'\nObject Data: {req.object.data}",
        requires=[req.capability],
        inputs=inputs,
    )

    result = engine.execute(contract)

    if not result.success:
        return ExecutionResponse(success=False, error=result.stderr or result.error_code or "Execution failed")

    # Determine output object type based on capability
    output_type_map = {
        "entity_extraction": "json",
        "text_analysis": "json",
        "transform": "text",
        "format": "text",
        "summarize": "text",
        "reasoning": "text",
        "coding": "code",
        "execution": "text",
    }

    new_obj = PointObject(
        id=str(uuid.uuid4()),
        type=output_type_map.get(req.capability, "text"),
        data=result.stdout,
        metadata={
            "source_capability": req.capability,
            "source_object_id": req.object.id,
            "duration": result.duration,
        },
    )

    return ExecutionResponse(success=True, new_object=new_obj)
