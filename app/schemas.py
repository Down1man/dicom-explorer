from pydantic import BaseModel
from typing import Optional, Dict, Any

class MetadataResponse(BaseModel):
    metadata: Dict[str, Any]
