"""
Centralized logging configuration for the Find Your Next Adventure application.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: str = "find_your_next_adventure.log",
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_output: bool = True
) -> None:
    """
    Set up centralized logging configuration for the entire application.
    
    Args:
        log_file: Name of the log file (default: find_your_next_adventure.log)
        log_level: Logging level (default: INFO)
        max_bytes: Maximum size of log file before rotation (default: 10MB)
        backup_count: Number of backup log files to keep (default: 5)
        console_output: Whether to also output logs to console (default: True)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Full path to log file
    log_path = log_dir / log_file
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (optional)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Log the setup
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - File: {log_path}, Level: {logging.getLevelName(log_level)}")
    
    # Suppress overly verbose logs from third-party libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_session_start(session_info: dict) -> None:
    """
    Log session start information.
    
    Args:
        session_info: Dictionary containing session information
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("SESSION STARTED")
    logger.info("=" * 60)
    
    for key, value in session_info.items():
        logger.info(f"{key}: {value}")
    
    logger.info("=" * 60)


def log_session_end(stats: dict) -> None:
    """
    Log session end information with statistics.
    
    Args:
        stats: Dictionary containing session statistics
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("SESSION ENDED")
    logger.info("=" * 60)
    
    for key, value in stats.items():
        logger.info(f"{key}: {value}")
    
    logger.info("=" * 60) 