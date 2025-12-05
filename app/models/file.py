from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.sql import func
from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    path = Column(String, nullable=False)
    size = Column(BigInteger, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uploaded_by = Column(Integer, nullable=False, default=1)
