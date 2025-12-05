from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.analysis import AnalysisOut
from app.models.analysis import Analysis as AnalysisModel
from app.services.analysis import run_analysis

router = APIRouter(prefix="/files", tags=["Analysis"])


@router.post(
    "/{file_id}/analyze",
    response_model=AnalysisOut,
    summary="Run AI analysis for file",
    description="Run AI-based analysis for the given file id and store the result",
)
async def analyze_file(file_id: int, db: Session = Depends(get_db)):
    analysis = await run_analysis(db, file_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="File not found")
    return analysis


@router.get(
    "/{file_id}/analysis",
    response_model=AnalysisOut,
    summary="Get latest analysis for file",
    description="Return the latest stored analysis for the given file id",
)
def get_file_analysis(file_id: int, db: Session = Depends(get_db)):
    analysis = (
        db.query(AnalysisModel)
        .filter(AnalysisModel.file_id == file_id)
        .order_by(AnalysisModel.analyzed_at.desc(), AnalysisModel.id.desc())
        .first()
    )
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
