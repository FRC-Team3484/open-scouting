import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

from ..utils import IS_DEV

router = APIRouter(
    tags=["Uploads"],
    include_in_schema=IS_DEV
)

UPLOAD_ROOT = Path(os.getenv("UPLOAD_ROOT", "/data/uploads"))
MAX_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Unsupported file type")

    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4()}{ext}"
    path = UPLOAD_ROOT / filename

    size = 0
    with path.open("wb") as f:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_SIZE:
                path.unlink(missing_ok=True)
                raise HTTPException(400, "File too large")
            f.write(chunk)

    return {
        "url": f"/uploads/{filename}",
        "filename": filename,
        "content_type": file.content_type,
        "size": size,
    }