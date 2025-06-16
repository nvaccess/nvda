# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Logging configuration for ART runtime processes."""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


def _getARTLogPath(addon_name: str) -> Path:
	"""Get the path for an ART addon's log file."""
	# Use the same logic as NVDA for finding the user data directory
	# This matches how NVDA determines its config path
	if os.environ.get("NVDA_ART_CONFIG_PATH"):
		# If explicitly set (e.g., for portable copies)
		base_dir = Path(os.environ["NVDA_ART_CONFIG_PATH"])
	else:
		# Use %APPDATA%\nvda\art for installed copies
		appdata = os.environ.get("APPDATA")
		if appdata:
			base_dir = Path(appdata) / "nvda" / "art"
		else:
			# Fallback to temp if APPDATA not available
			import tempfile
			base_dir = Path(tempfile.gettempdir()) / "nvda" / "art"
	
	log_dir = base_dir / "logs"
	
	# Create directory if it doesn't exist
	log_dir.mkdir(parents=True, exist_ok=True)
	
	# Sanitize addon name for filename
	safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in addon_name)
	return log_dir / f"{safe_name}.log"


def cleanupOldLogs(addon_name: str, days_to_keep: int = 7):
	"""Clean up old ART log files.
	
	@param addon_name: Name of the addon
	@param days_to_keep: Number of days to keep logs
	"""
	import time
	
	log_path = _getARTLogPath(addon_name)
	log_dir = log_path.parent
	
	if not log_dir.exists():
		return
		
	current_time = time.time()
	cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
	
	# Clean up old logs for this addon
	pattern = f"art_{addon_name}*.log*"
	for log_file in log_dir.glob(pattern):
		try:
			if log_file.stat().st_mtime < cutoff_time:
				log_file.unlink()
		except Exception:
			pass  # Ignore errors during cleanup


def configureLogging(addon_name: str, debug: bool = False) -> logging.Logger:
	"""Configure logging for an ART process.
	
	@param addon_name: Name of the addon this ART process is running
	@param debug: Whether to enable debug logging
	@return: The configured logger for ART
	"""
	# Clean up old logs first
	cleanupOldLogs(addon_name)
	
	# Create a logger specific to this ART instance
	logger = logging.getLogger(f"ART.{addon_name}")
	logger.setLevel(logging.DEBUG if debug else logging.INFO)
	
	# Remove any existing handlers
	logger.handlers.clear()
	
	# File handler with rotation
	log_path = _getARTLogPath(addon_name)
	try:
		file_handler = logging.handlers.RotatingFileHandler(
			log_path,
			maxBytes=1024 * 1024,  # 1MB
			backupCount=3,
			encoding='utf-8'
		)
		
		# Format: timestamp - level - logger - message
		formatter = logging.Formatter(
			'%(asctime)s - %(levelname)s - %(name)s - %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
		
	except Exception as e:
		# If we can't create file handler, fall back to stderr
		print(f"Failed to create log file at {log_path}: {e}", file=sys.stderr)
		stderr_handler = logging.StreamHandler(sys.stderr)
		stderr_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
		logger.addHandler(stderr_handler)
	
	# Also log to stderr in debug mode
	if debug:
		stderr_handler = logging.StreamHandler(sys.stderr)
		stderr_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
		logger.addHandler(stderr_handler)
	
	# Log startup info
	logger.info(f"ART logging initialized for addon: {addon_name}")
	logger.info(f"Log file: {log_path}")
	logger.info(f"Debug mode: {debug}")
	logger.info(f"Python version: {sys.version}")
	
	return logger


def getLogger(name: str) -> logging.Logger:
	"""Get a logger for ART components.
	
	@param name: Logger name (will be prefixed with 'ART.')
	@return: Logger instance
	"""
	if not name.startswith("ART."):
		name = f"ART.{name}"
	return logging.getLogger(name)
