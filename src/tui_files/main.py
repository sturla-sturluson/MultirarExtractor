from .string_colourer import String_Colourer as SC
from .common import get_cleanup_info_string
from ..utils import get_all_rar_files_in_tree
from pathlib import Path
from ..extraction import extract_7z_file, delete_rar_files



def exctract_and_delete_script(folderpath:str):
    rar_list = get_all_rar_files_in_tree(folderpath)

    for rarfile in rar_list:
        cleanup_files = extract_7z_file(rarfile)
        information_string = get_cleanup_info_string(cleanup_files)
        print(information_string)
        message = delete_rar_files(cleanup_files)
        # found_files = find_extracted_videos(rarfile.parent)
        # found_names = format_extracted_video_names(found_files)
        # print(f"{SC.GREEN}{found_names}{SC.END}")
        # print(f"{SC.RED}{information_string}{SC.END}")



def run_extraction(folderpath:str):
    exctract_and_delete_script(folderpath)
