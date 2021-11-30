from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class GenerateStatus(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0
    result: list = []
