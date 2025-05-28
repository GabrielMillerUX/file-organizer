#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from config import Config
from logger import FileOrganizerLogger

class FileOrganizer:
    def __init__(self):
        self.config = Config()
        self.logger = FileOrganizerLogger()
        self.source_dir = None
        self.target_dir = None
        self.file_categories = self.config.get_file_categories()
        
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
            self.logger.log_error("Source and target directories must be set")
            raise ValueError("Source and target directories must be set")
        
        if not self.source_dir.exists():
            self.logger.log_error(f"Source directory does not exist: {self.source_dir}")
            raise FileNotFoundError(f"Source directory does not exist: {self.source_dir}")
        
        if not self.target_dir.exists():
            self.logger.log_error(f"Target directory does not exist: {self.target_dir}")
            raise FileNotFoundError(f"Target directory does not exist: {self.target_dir}")
        
        self.logger.log_operation_start(self.source_dir, self.target_dir)
        self.config.update_last_dirs(self.source_dir, self.target_dir)
            
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
                    self.logger.log_file_moved(file_path, dest_path, category)
                    files_moved += 1
                except Exception as e:
                    self.logger.log_file_error(file_path, str(e))
                    continue
        
        self.logger.log_operation_complete(files_moved)
        return files_moved


def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("600x450")
    
    organizer = FileOrganizer()
    
    # Labels and buttons
    tk.Label(root, text="File Organizer", font=("Arial", 16, "bold")).pack(pady=10)
    
    source_frame = tk.Frame(root)
    source_frame.pack(pady=10)
    tk.Label(source_frame, text="Source Directory:").pack(side=tk.LEFT)
    source_label = tk.Label(source_frame, text="Not selected", fg="gray")
    source_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def select_source():
        initial_dir = organizer.config.config.get('last_source_dir', '')
        folder = filedialog.askdirectory(title="Select Source Folder", initialdir=initial_dir)
        if folder:
            organizer.set_source_directory(folder)
            source_label.config(text=folder, fg="black")
            update_preview()
    
    tk.Button(root, text="Select Source Folder", command=select_source).pack(pady=5)
    
    target_frame = tk.Frame(root)
    target_frame.pack(pady=10)
    tk.Label(target_frame, text="Target Directory:").pack(side=tk.LEFT)
    target_label = tk.Label(target_frame, text="Not selected", fg="gray")
    target_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def select_target():
        initial_dir = organizer.config.config.get('last_target_dir', '')
        folder = filedialog.askdirectory(title="Select Target Folder", initialdir=initial_dir)
        if folder:
            organizer.set_target_directory(folder)
            target_label.config(text=folder, fg="black")
    
    tk.Button(root, text="Select Target Folder", command=select_target).pack(pady=5)
    
    # Preview area
    preview_frame = tk.Frame(root)
    preview_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    tk.Label(preview_frame, text="Files to organize:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    
    preview_text = tk.Text(preview_frame, height=8, width=70)
    preview_scrollbar = tk.Scrollbar(preview_frame)
    preview_text.config(yscrollcommand=preview_scrollbar.set)
    preview_scrollbar.config(command=preview_text.yview)
    
    preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_preview():
        preview_text.delete(1.0, tk.END)
        if organizer.source_dir and organizer.source_dir.exists():
            file_count = {}
            for file_path in organizer.source_dir.iterdir():
                if file_path.is_file():
                    category = organizer.get_file_category(file_path)
                    file_count[category] = file_count.get(category, 0) + 1
            
            if file_count:
                preview_text.insert(tk.END, "Files found by category:\n\n")
                for category, count in sorted(file_count.items()):
                    preview_text.insert(tk.END, f"{category}: {count} files\n")
            else:
                preview_text.insert(tk.END, "No files found in source directory.")
        else:
            preview_text.insert(tk.END, "Please select a source directory first.")
    
    def organize():
        try:
            files_moved = organizer.organize_files()
            messagebox.showinfo("Success", f"Successfully organized {files_moved} files!")
            update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    tk.Button(root, text="Organize Files", command=organize, 
              bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()