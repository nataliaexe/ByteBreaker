"""
Advanced logging module for ByteBreaker Framework
"""
import logging
import logging.handlers
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import sys
import os


class ByteBreakerLogger:
    """Custom logger with multiple handlers"""
    
    def __init__(self, name: str = "ByteBreaker", log_dir: str = "data/logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler()
        self._setup_json_handler()
        self._setup_error_handler()
    
    def _setup_console_handler(self) -> None:
        """Setup console output handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self) -> None:
        """Setup file output handler"""
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "bytebreaker.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
    
    def _setup_json_handler(self) -> None:
        """Setup JSON format handler for machine parsing"""
        json_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "bytebreaker.json",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        json_handler.setLevel(logging.INFO)
        
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.now().isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "line": record.lineno
                }
                if hasattr(record, 'extra_data'):
                    log_data.update(record.extra_data)
                return json.dumps(log_data)
        
        json_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(json_handler)
    
    def _setup_error_handler(self) -> None:
        """Setup error file handler"""
        error_handler = logging.FileHandler(self.log_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        
        error_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'File: %(filename)s:%(lineno)d\n'
            'Function: %(funcName)s\n'
        )
        error_handler.setFormatter(error_format)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message"""
        self.logger.debug(message, extra={"extra_data": extra} if extra else None)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log info message"""
        self.logger.info(message, extra={"extra_data": extra} if extra else None)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message"""
        self.logger.warning(message, extra={"extra_data": extra} if extra else None)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log error message"""
        self.logger.error(message, extra={"extra_data": extra} if extra else None)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log critical message"""
        self.logger.critical(message, extra={"extra_data": extra} if extra else None)
