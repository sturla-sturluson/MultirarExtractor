from .string_colourer import String_Colourer as SC
from ..utils import format_size, is_multi_rar_extension
from pathlib import Path
from ..constants import NEWLINE
import os

def get_user_confirm(num_of_files: int) -> bool:
    """Get user confirmation to delete files."""
    answer = input(
        f"{SC.RED}{SC.BOLD}{num_of_files}{SC.END}{SC.YELLOW} files to delete.\n Do you want to continue? (c){SC.END}\n$: ").strip().lower()
    if answer == "c":
        return True
    return False

# def delete_confirm_prompt(number_of_files:int)->str:
#     return get_user_confirm(number_of_files)

def get_file_string(filename: Path):
    filestring = str()
    filestring += f"Name: {str(filename.name)} "
    stats = filename.stat()
    filestring += f"Size: {format_size(stats.st_size)}"
    return filestring

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def show_file_list(cleanup_files: list[Path]) -> tuple[list[Path], list[Path]]:
    show_list = list()
    multi_rar_list = list()
    current_multi_rar = ""
    for file in cleanup_files:
        if is_multi_rar_extension(file.suffix):
            if file.suffix == ".r00":
                multi_rar_list.append(file)
            else:
                current_multi_rar = file
        else:
            show_list.append(file)

    multi_rar_list.append(current_multi_rar)

    return show_list, multi_rar_list



def get_cleanup_info_string(cleanup_files: list[Path]) -> str:
    """Finds files to be deleted and returns a formatted string"""
    show_list, multi_rar_list = show_file_list(cleanup_files)
    information_string = ""
    # Foldername
    if len(show_list) > 0:
        information_string = f"Folder: {str(show_list[0].parent)}{NEWLINE}"
    for index, filename in enumerate(show_list):
        information_string += f"\t{index+1}. {str(filename.name)}{NEWLINE}"
    if len(multi_rar_list) > 1:
        information_string += f"\t {str(multi_rar_list[0].name)}{NEWLINE}"
        information_string += "\t......" + NEWLINE
        information_string += f"\t {str(multi_rar_list[1].name)}{NEWLINE}"
    return information_string
