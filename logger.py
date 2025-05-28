import logging
import os
from pathlib import Path
from datetime import datetime

class FileOrganizerLogger:
    def __init__(self):
        self.log_dir = Path.home() / '.file_organizer_logs'
        self.log_dir.mkdir(exist_ok=True)
        
        log_file = self.log_dir / f'file_organizer_{datetime.now().strftime("%Y%m%d")}.log'
        
        # Setup logger
        self.logger = logging.getLogger('FileOrganizer')
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_operation_start(self, source_dir, target_dir):
        self.logger.info(f"Starting file organization: {source_dir} -> {target_dir}")
    
    def log_file_moved(self, source_path, dest_path, category):
        self.logger.info(f"Moved [{category}] {source_path} -> {dest_path}")
    
    def log_file_error(self, file_path, error):
        self.logger.error(f"Failed to move {file_path}: {error}")
    
    def log_operation_complete(self, files_moved):
        self.logger.info(f"Organization complete. {files_moved} files moved successfully.")
    
    def log_warning(self, message):
        self.logger.warning(message)
    
    def log_error(self, message):
        self.logger.error(message)