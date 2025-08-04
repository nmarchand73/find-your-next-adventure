"""File I/O utilities."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)


def save_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: Data to save
        file_path: Path to save the file
        indent: JSON indentation level

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        logger.info(f"Successfully saved JSON to: {file_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        return False


def load_json(file_path: Union[str, Path]) -> Union[Dict, List, None]:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Loaded data or None if failed
    """
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            logger.error(f"JSON file not found: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"Successfully loaded JSON from: {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        return None


def ensure_directory(directory: Union[str, Path]) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path to ensure

    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes, or -1 if error
    """
    try:
        return Path(file_path).stat().st_size
    except Exception:
        return -1


def backup_file(file_path: Union[str, Path], backup_suffix: str = ".backup") -> bool:
    """
    Create a backup copy of a file.

    Args:
        file_path: Path to the file to backup
        backup_suffix: Suffix to add to backup file

    Returns:
        True if backup was created, False otherwise
    """
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            logger.warning(f"Cannot backup non-existent file: {file_path}")
            return False

        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)

        # Copy file content
        with open(file_path, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())

        logger.info(f"Created backup: {backup_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to backup {file_path}: {e}")
        return False
