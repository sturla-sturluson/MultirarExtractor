from pathlib import Path
from ..utils import find_cleanup_files, find_extracted_file
from ..tkinter_files.models import FoundRarFile
import os
import subprocess
import re
import threading

def run_async_extraction(rarfile: FoundRarFile):
    # Convert string path to Path object (if needed)
    # Create a thread to run the extraction
    extraction_thread = threading.Thread(target=extract_7z_file_thread, args=(rarfile,))
    extraction_thread.start()
    return extraction_thread

def extract_7z_file_thread(rarfile: FoundRarFile):
    """Extracts a 7z file and returns the output"""
    # script_path = create_7z_extract_script(filepath)
    # run_script(script_path)
    extract_command = get_script_command(rarfile.path)
    os.system(extract_command)

def extract_7z_file(filepath: Path) -> list[Path]:
    """Extracts a 7z file and returns the output"""
    # script_path = create_7z_extract_script(filepath)
    # run_script(script_path)
    extract_command = get_script_command(filepath)
    os.system(extract_command)
    
    return find_cleanup_files(filepath)


def get_script_command(filepath: Path) -> str:
    """Gets a 7zip extract console command
    Example: 7z x "C://Users//user//Downloads//file.rar" -o"C://Users//user//Downloads//"
    """
    _safe_filepath = str(filepath).replace("\\", "//")
    _safe_parent = str(filepath.parent).replace("\\", "//")

    return f"7z x \"{_safe_filepath}\" -o\"{_safe_parent}\""

def delete_rar_files(cleanup_files: list[Path]) -> int:
    """Deletes all files in the list returns number of files deleted"""
    count = 0
    for file in cleanup_files:
        count += 1
        #delete_file(file)
    return count



