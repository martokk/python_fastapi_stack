import os
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile, HTTPException
import magic  # python-magic library for file type detection

UPLOAD_DIR = Path("app/static/uploads")


async def validate_image(file: UploadFile) -> None:
    content = await file.read()
    file.file.seek(0)  # Reset file pointer

    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(content)

    if not file_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")


async def save_upload(file: UploadFile, subfolder: str) -> str:
    """
    Save an uploaded file and return its URL path
    """
    await validate_image(file)

    # Limit file size to 5MB
    if len(await file.read()) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size too large (max 5MB)")
    file.file.seek(0)

    # Create upload directory if it doesn't exist
    upload_dir = UPLOAD_DIR / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid4()}{file_extension}"

    # Save file
    file_path = upload_dir / filename
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Return URL path
    return f"/static/uploads/{subfolder}/{filename}"
