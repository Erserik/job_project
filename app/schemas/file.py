from datetime import datetime
from pydantic import BaseModel


class FileOut(BaseModel):
    id: int
    original_name: str
    version: int
    path: str
    size: int
    uploaded_at: datetime
    uploaded_by: int

    class Config:
        from_attributes = True
