from datetime import datetime
from pydantic import BaseModel


class AnalysisOut(BaseModel):
    id: int
    file_id: int
    version: int
    analysis_text: str
    analyzed_at: datetime

    class Config:
        from_attributes = True
