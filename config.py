import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_file = Path.home() / '.file_organizer_config.json'
        self.default_config = {
            'file_categories': {
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
                'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
                'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
                'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
                'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go']
            },
            'last_source_dir': '',
            'last_target_dir': '',
            'auto_create_folders': True
        }
        self.config = self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def get_file_categories(self):
        return self.config.get('file_categories', self.default_config['file_categories'])
    
    def update_last_dirs(self, source_dir, target_dir):
        self.config['last_source_dir'] = str(source_dir) if source_dir else ''
        self.config['last_target_dir'] = str(target_dir) if target_dir else ''
        self.save_config()