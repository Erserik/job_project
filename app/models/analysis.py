from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    version = Column(Integer, nullable=False)
    analysis_text = Column(String, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
