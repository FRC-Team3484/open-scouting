import os
import uuid
from pathlib import Path
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
import pillow_heif

from ..models import Profile
from ..dependencies import Identity, require_user

from ..utils import IS_DEV

pillow_heif.register_heif_opener()

router = APIRouter(
    tags=["Uploads"],
    include_in_schema=IS_DEV
)

UPLOAD_ROOT = Path(os.getenv("UPLOAD_ROOT", "/data/uploads"))

# Normal images
MAX_SIZE = 10 * 1024 * 1024  # per-file
MAX_WIDTH = 1080

# Profile Pictures
MAX_PROFILE_PICTURE_WIDTH = 256

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heic",
    "image/heif",
}

@router.post("/upload/image")
async def upload_image(
    file_uuid: str,
    file: UploadFile = File(...),
):
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

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
    filename = f"{file_uuid}.png"
    path = UPLOAD_ROOT / filename
    img.save(path, format="PNG", optimize=True)

    print("Created image:", path)

    return {
        "original_filename": file.filename,
        "filename": filename,
        "url": f"/uploads/{filename}",
        "width": img.width,
        "height": img.height,
        "size": path.stat().st_size,
    }

@router.post("/upload/profile_picture/me")
async def upload_profile_picture(file: UploadFile = File(...), identity: Identity = Depends(require_user)):
    """
    Given the uploaded file, store it on the server

    Use the generated URL to assign the image to the user's profile

    Return the relevant image information
    """
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

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
    if img.width > MAX_PROFILE_PICTURE_WIDTH:
        img = img.resize(
            (MAX_PROFILE_PICTURE_WIDTH, MAX_PROFILE_PICTURE_WIDTH),
            Image.Resampling.LANCZOS
        )

    # Save as PNG
    filename = f"{uuid.uuid4()}.png"
    path = UPLOAD_ROOT / filename
    img.save(path, format="PNG", optimize=True)

    print("Created profile picture:", path)

    # Get user profile
    profile: Profile | None = await Profile.get_or_none(user=identity.user)
    if not profile:
        profile = await Profile.create(user=identity.user, created_by=identity.session)

    # If user has old profile picture, delete it
    if profile.profile_picture_url:
        old_path = Path(profile.profile_picture_url)
        if old_path.exists():
            old_path.unlink()

    # Assign image to user profile
    profile.profile_picture_url = UPLOAD_ROOT / filename
    await profile.save()

    return {
        "original_filename": file.filename,
        "filename": filename,
        "url": f"/uploads/{filename}",
        "width": img.width,
        "height": img.height,
        "size": path.stat().st_size,
    }