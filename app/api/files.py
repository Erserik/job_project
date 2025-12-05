from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.file import File as FileModel
from app.schemas.file import FileOut


router = APIRouter(prefix="/files", tags=["Files"])

storage_dir = Path(settings.storage_path)
storage_dir.mkdir(parents=True, exist_ok=True)


def get_next_version(db: Session, original_name: str) -> int:
    last_file = (
        db.query(FileModel)
        .filter(FileModel.original_name == original_name)
        .order_by(FileModel.version.desc())
        .first()
    )
    if last_file:
        return last_file.version + 1
    return 1


def build_versioned_filename(original_name: str, version: int) -> str:
    path = Path(original_name)
    if version == 1:
        return original_name
    return f"{path.stem}_v{version}{path.suffix}"


@router.post(
    "/upload",
    response_model=FileOut,
    summary="Upload file",
    description="Upload file with automatic versioning and store metadata",
)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    version = get_next_version(db, file.filename)
    versioned_name = build_versioned_filename(file.filename, version)
    save_path = storage_dir / versioned_name

    try:
        save_path.write_bytes(data)
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to save file")

    db_file = FileModel(
        original_name=file.filename,
        version=version,
        path=str(save_path),
        size=len(data),
        uploaded_by=1,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get(
    "",
    response_model=List[FileOut],
    summary="List files",
    description="List all stored files with versions and metadata",
)
def list_files(db: Session = Depends(get_db)):
    files = (
        db.query(FileModel)
        .order_by(FileModel.uploaded_at.desc(), FileModel.id.desc())
        .all()
    )
    return files
