# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 15:25:32 2024

@author: Erick
"""

import os
import shutil
import exifread

def get_image_metadata(file_path):
    """Extract metadata (like date taken) from an image."""
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            # Assuming the DateTimeOriginal tag is a unique identifier for the photo
            date_taken = tags.get('EXIF DateTimeOriginal')
            return str(date_taken)
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None

def find_unique_files(dir1, dir2, output_dir):
    # Define supported formats for photos and videos
    supported_formats = (
        '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.heic', '.heif', '.nef', '.cr2', '.arw', '.dng', '.orf',
        '.raf', '.sr2', '.rw2', '.3gp', '.avi', '.flv', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.mts', '.mxf', 
        '.ogg', '.rm', '.swf', '.vob', '.webm', '.wmv'
    )
    
    # Create a set of metadata strings for files in each directory
    metadata_set1 = set()
    metadata_set2 = set()
    
    # Traverse the first directory and collect metadata
    for root, _, files in os.walk(dir1):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                metadata = get_image_metadata(file_path)
                if metadata:
                    metadata_set1.add(metadata)
    
    # Traverse the second directory and collect metadata
    for root, _, files in os.walk(dir2):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                metadata = get_image_metadata(file_path)
                if metadata:
                    metadata_set2.add(metadata)

    # Find unique files in both directories
    unique_in_dir1 = metadata_set1 - metadata_set2
    unique_in_dir2 = metadata_set2 - metadata_set1

    # Copy unique files to the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(dir1):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                metadata = get_image_metadata(file_path)
                if metadata in unique_in_dir1:
                    shutil.copy2(file_path, os.path.join(output_dir, file))

    for root, _, files in os.walk(dir2):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                metadata = get_image_metadata(file_path)
                if metadata in unique_in_dir2:
                    shutil.copy2(file_path, os.path.join(output_dir, file))

# Define the directories to compare
dir1 = 'E:\\Photos'
dir2 = 'D:\\OneDrive\Photos'
output_dir = 'E:\\unicas'

find_unique_files(dir1, dir2, output_dir)