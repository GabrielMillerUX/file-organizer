#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

class FileOrganizer:
    def __init__(self):
        self.source_dir = None
        self.target_dir = None
        self.file_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']
        }
        
    def set_source_directory(self, path):
        self.source_dir = Path(path)
        
    def set_target_directory(self, path):
        self.target_dir = Path(path)
        
    def get_file_category(self, file_path):
        file_ext = file_path.suffix.lower()
        for category, extensions in self.file_categories.items():
            if file_ext in extensions:
                return category
        return 'other'
        
    def organize_files(self):
        if not self.source_dir or not self.target_dir:
            raise ValueError("Source and target directories must be set")
            
        files_moved = 0
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path)
                category_dir = self.target_dir / category
                category_dir.mkdir(exist_ok=True)
                
                dest_path = category_dir / file_path.name
                shutil.move(str(file_path), str(dest_path))
                files_moved += 1
                
        return files_moved


def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("500x300")
    
    # TODO: add GUI components
    
    root.mainloop()

if __name__ == "__main__":
    main()