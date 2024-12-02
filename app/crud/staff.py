import re
from pathlib import Path

from fastapi import UploadFile

from app import models
from app.paths import UPLOAD_PATH

from .base import BaseCRUD


class StaffCRUD(BaseCRUD[models.Staff, models.StaffCreate, models.StaffUpdate]):
    async def save_photo(self, photo: UploadFile | None, staff_name: str) -> str | None:
        """Save photo and return the URL path"""
        if not photo or not photo.filename:
            return None

        # Create upload directory if it doesn't exist
        upload_dir = UPLOAD_PATH / "staff"
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Create filename from staff name
        safe_name = re.sub(r"[^a-zA-Z0-9]", "_", staff_name.lower().strip())
        file_extension = Path(photo.filename).suffix
        file_name = f"{safe_name}{file_extension}"
        file_path = upload_dir / file_name

        # Save the file
        content = await photo.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Return the URL path
        return f"/uploads/staff/{file_name}"

    async def delete_photo(self, photo_url: str) -> None:
        """Delete photo file"""
        if not photo_url:
            return

        try:
            # Get the file path from the URL
            file_name = photo_url.split("/")[-1]
            file_path = UPLOAD_PATH / "staff" / file_name

            # Delete the file if it exists
            if file_path.is_file():
                file_path.unlink()
        except Exception as e:
            print(f"Error deleting photo: {e}")


staff = StaffCRUD(model=models.Staff)
