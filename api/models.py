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
