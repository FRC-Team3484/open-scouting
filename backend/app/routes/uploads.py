import os
import uuid
from pathlib import Path
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import pillow_heif

from ..utils import IS_DEV

pillow_heif.register_heif_opener()

router = APIRouter(
    tags=["Uploads"],
    include_in_schema=IS_DEV
)

UPLOAD_ROOT = Path(os.getenv("UPLOAD_ROOT", "/data/uploads"))
MAX_SIZE = 10 * 1024 * 1024  # per-file
MAX_WIDTH = 1080

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heic",
    "image/heif",
}

@router.post("/upload/images")
async def upload_images(
    files: list[UploadFile] = File(...)
):
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

    results = []

    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, f"Unsupported file type: {file.filename}")

        # Read file with size limit
        size = 0
        data = bytearray()

        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_SIZE:
                raise HTTPException(400, f"File too large: {file.filename}")
            data.extend(chunk)

        # Open image safely
        try:
            img = Image.open(BytesIO(data))
            img.load()
        except Exception:
            raise HTTPException(400, f"Invalid image: {file.filename}")

        # Normalize mode
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Resize if needed
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            img = img.resize(
                (MAX_WIDTH, int(img.height * ratio)),
                Image.Resampling.LANCZOS
            )

        # Save as PNG
        filename = f"{uuid.uuid4()}.png"
        path = UPLOAD_ROOT / filename
        img.save(path, format="PNG", optimize=True)

        results.append({
            "original_filename": file.filename,
            "filename": filename,
            "url": f"/uploads/{filename}",
            "width": img.width,
            "height": img.height,
            "size": path.stat().st_size,
        })

    return {
        "count": len(results),
        "files": results,
    }