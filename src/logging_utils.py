"""
Logging utilities for SNA project.
Provides consistent logging across all modules.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from src.config import LOGS_DIR, LOGGING_CONFIG


def setup_logging(module_name: str, log_to_file: bool = True) -> logging.Logger:
    """
    Setup logger with both console and file handlers.
    
    Args:
        module_name: Name of the module (usually __name__)
        log_to_file: Whether to also log to file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(module_name)
    
    # Avoid duplicate handlers if logger already configured
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(LOGGING_CONFIG["level"])
    
    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler (optional)
    file_handler = None
    if log_to_file:
        log_file = LOGS_DIR / f"{module_name}_{datetime.now():%Y%m%d_%H%M%S}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        LOGGING_CONFIG["format"],
        datefmt=LOGGING_CONFIG["date_format"]
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if file_handler:
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass


def validate_dataframe_structure(df, required_columns: list, logger=None) -> bool:
    """
    Validate DataFrame has required columns and no critical nulls.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        logger: Optional logger for warnings
        
    Returns:
        True if valid
        
    Raises:
        DataValidationError: If validation fails
    """
    import pandas as pd
    
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError("Input must be a pandas DataFrame")
    
    if df.empty:
        raise DataValidationError("DataFrame is empty")
    
    # Check required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise DataValidationError(f"Missing required columns: {missing_cols}")
    
    # Check for null values in critical columns
    for col in required_columns:
        null_count = df[col].isna().sum()
        if null_count > 0:
            msg = f"Column '{col}' has {null_count} null values"
            if logger:
                logger.warning(msg)
            else:
                print(f"WARNING: {msg}")
    
    return True
