import os
from pathlib import Path

from fastapi import UploadFile

from app import models
from app.core.uuid import generate_uuid_random
from app.paths import UPLOAD_PATH

from .base import BaseCRUD


class PartnerCRUD(BaseCRUD[models.Partner, models.PartnerCreate, models.PartnerUpdate]):
    async def save_photo(self, photo: UploadFile, name: str) -> str:
        """Save partner logo and return the URL"""
        # Create partners directory if it doesn't exist
        upload_dir = UPLOAD_PATH / "partners"
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        ext = os.path.splitext(photo.filename)[1]
        filename = f"{name.lower().replace(' ', '_')}{ext}"
        file_path = upload_dir / filename

        # Save file
        content = await photo.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Return URL path
        return f"/uploads/partners/{filename}"

    async def delete_photo(self, photo_url: str) -> None:
        """Delete partner logo file"""
        if not photo_url:
            return

        # Get file path from URL
        filename = photo_url.split("/")[-1]
        file_path = UPLOAD_PATH / "partners" / filename

        # Delete file if it exists
        if file_path.exists():
            file_path.unlink()


partner = PartnerCRUD(model=models.Partner)
