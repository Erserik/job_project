from pathlib import Path
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.file import File as FileModel
from app.models.analysis import Analysis as AnalysisModel
from app.utils.ai import analyze_metadata


async def run_analysis(db: Session, file_id: int) -> Optional[AnalysisModel]:
    db_file = (
        db.query(FileModel)
        .filter(FileModel.id == file_id)
        .first()
    )

    if not db_file:
        return None

    path = Path(db_file.path)
    metadata: Dict[str, Any] = {
        "file_id": db_file.id,
        "file_name": db_file.original_name,
        "file_size": db_file.size,
        "version": db_file.version,
        "extension": path.suffix,
        "uploaded_at": db_file.uploaded_at.isoformat() if db_file.uploaded_at else None,
    }

    text = await analyze_metadata(metadata)

    analysis = AnalysisModel(
        file_id=db_file.id,
        version=db_file.version,
        analysis_text=text,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis
