import os
from pathlib import Path
import logging


async def cleanup_file(file_path: str) -> None:
    """Delete file if it exists"""
    try:
        if file_path and file_path.startswith("/static/uploads/"):
            full_path = Path("app") / file_path.lstrip("/")
            if full_path.exists():
                os.remove(full_path)
    except Exception as e:
        logging.error(f"Error cleaning up file {file_path}: {str(e)}")
