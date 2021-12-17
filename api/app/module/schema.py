from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Dict
from pydantic import UUID4

class GenerateStatus(BaseModel):
    uid: UUID4 = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0

jobs: Dict[UUID4, GenerateStatus] = {}
