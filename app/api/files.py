from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.file import File as FileModel
from app.schemas.file import FileOut

router = APIRouter(prefix="/files", tags=["Files"])

storage_dir = Path(settings.storage_path)
storage_dir.mkdir(parents=True, exist_ok=True)


@router.post(
    "/upload",
    response_model=FileOut,
    summary="Upload file",
    description="Upload file and store its metadata",
)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    save_path = storage_dir / file.filename

    try:
        save_path.write_bytes(data)
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to save file")

    db_file = FileModel(
        original_name=file.filename,
        version=1,
        path=str(save_path),
        size=len(data),
        uploaded_by=1,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file
