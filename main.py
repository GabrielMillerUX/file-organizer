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
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory does not exist: {self.source_dir}")
        
        if not self.target_dir.exists():
            raise FileNotFoundError(f"Target directory does not exist: {self.target_dir}")
            
        files_moved = 0
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                try:
                    category = self.get_file_category(file_path)
                    category_dir = self.target_dir / category
                    category_dir.mkdir(exist_ok=True)
                    
                    dest_path = category_dir / file_path.name
                    
                    # Handle duplicate filenames
                    counter = 1
                    while dest_path.exists():
                        name_parts = file_path.stem, counter, file_path.suffix
                        dest_path = category_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(dest_path))
                    files_moved += 1
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
                    continue
                
        return files_moved


def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("500x350")
    
    organizer = FileOrganizer()
    
    # Labels and buttons
    tk.Label(root, text="File Organizer", font=("Arial", 16, "bold")).pack(pady=10)
    
    source_frame = tk.Frame(root)
    source_frame.pack(pady=10)
    tk.Label(source_frame, text="Source Directory:").pack(side=tk.LEFT)
    source_label = tk.Label(source_frame, text="Not selected", fg="gray")
    source_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def select_source():
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            organizer.set_source_directory(folder)
            source_label.config(text=folder, fg="black")
    
    tk.Button(root, text="Select Source Folder", command=select_source).pack(pady=5)
    
    target_frame = tk.Frame(root)
    target_frame.pack(pady=10)
    tk.Label(target_frame, text="Target Directory:").pack(side=tk.LEFT)
    target_label = tk.Label(target_frame, text="Not selected", fg="gray")
    target_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def select_target():
        folder = filedialog.askdirectory(title="Select Target Folder")
        if folder:
            organizer.set_target_directory(folder)
            target_label.config(text=folder, fg="black")
    
    tk.Button(root, text="Select Target Folder", command=select_target).pack(pady=5)
    
    def organize():
        try:
            files_moved = organizer.organize_files()
            messagebox.showinfo("Success", f"Successfully organized {files_moved} files!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    tk.Button(root, text="Organize Files", command=organize, 
              bg="green", fg="white", font=("Arial", 12)).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()