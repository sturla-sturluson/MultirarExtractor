from pathlib import Path
from ..constants import *
import json
from ..tkinter_files.models import SavedPath, FoundRarFile
import os
from .common import get_file_string, is_multi_rar_extension
from ..constants import UTF_8, VIDEO_EXTENSIONS

IGNORE_DIR = ["venv",]
IGNORE_IF_STARTS = ["__", "."]
CWD = Path.cwd()

_DEFAULT_CONFIG_JSON = {
    SAVED_PATHS: [],
    DELETE_TOGGLED: False,
    EXTRACT_TOGGLED: False
    

}

def _create_path(file_path: Path, create_file:bool) -> None:
    """Creates the path to the file, including all intermediate directories"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if create_file and not file_path.exists():
        with open(file_path, "w") as file:
            json.dump(_DEFAULT_CONFIG_JSON, file)



def get_config_json() -> dict:
    """Reads the config.json file and returns the contents as a dictionary"""
    _create_path(Path(CONFIG_JSON), True)
    _list_of_saved_path_dicts = []
    _data = dict()
    try:
        with open(CONFIG_JSON, "r") as file:
            data = json.load(file)
            for path in data[SAVED_PATHS]:
                _list_of_saved_path_dicts.append(SavedPath(**path))
    except json.JSONDecodeError:
        save_config_json(_DEFAULT_CONFIG_JSON)
        _data = _DEFAULT_CONFIG_JSON
    
    _data[SAVED_PATHS] = _list_of_saved_path_dicts
    _data[DELETE_TOGGLED] = data.get(DELETE_TOGGLED, False)
    _data[EXTRACT_TOGGLED] = data.get(EXTRACT_TOGGLED, False)
    return _data
    
def save_config_json(data: dict) -> None:
    """Writes the data to the config.json file"""
    _create_path(Path(CONFIG_JSON), True)
    data[SAVED_PATHS] = [saved_path.__dict__() for saved_path in data[SAVED_PATHS]]
    with open(CONFIG_JSON, "w") as file:
        json.dump(data, file, indent=4)

    
def find_extracted_videos(folderpath: Path) -> list[Path]:
    """Finds all video files in the folderpath and returns a list paths to the files"""
    found_files = list()
    all_files = get_all_filesnames_in_tree(folderpath)
    for file in all_files:
        extension = file.suffix
        if str(extension).strip(".") in VIDEO_EXTENSIONS:
            found_files.append(file)
    return found_files

def create_directory(filepath: str|Path) -> None:
    """Creates the directory and/or the entire path if it does not exist"""
    checked_path = Path(filepath)
    # Checks if the filepath is a file, if it is changes the path to end at the parent directory
    if checked_path.is_file:
        checked_path = checked_path.parent

    checked_path.mkdir(parents=True, exist_ok=True)


def get_all_filesnames_in_tree(filepath: Path) -> list[Path]:
    """
    Walks the directory provided and returns a list of all the files
    Walks all subdirectories
    """
    filepath_list = list()
    for dir, subdirs, files in os.walk(str(filepath)):
        for file in files:
            if is_ignored_file(Path(file)):
                continue
            filepath_list.append(Path(dir).joinpath(file))
            
    return filepath_list

def get_all_directory_filenames(filepath: Path|str) -> list[Path]:
    """Walks the directory provided and returns a list of all the files
        Does not walk subdirectories"""
    filepath_list = list()
    for dir, _, files in os.walk(str(filepath)):
        for file in files:
            if is_ignored_file(Path(file)):
                continue
            filepath_list.append(Path(dir).joinpath(file))
    return filepath_list


def is_ignored_file(filepath: Path) -> bool:
    """Checks if the directory should be ignored or not"""
    if type(filepath) == str:
        filepath = Path(filepath)
    if filepath.is_file():
        filename = filepath.stem
        filename.strip().lower()
        for prefix in IGNORE_IF_STARTS:
            if filename.startswith(prefix):
                return True
    return False


def is_ignored_dir(filepath: Path) -> bool:
    """Checks if the directory should be ignored or not"""
    if type(filepath) == str:
        filepath = Path(filepath)
    if filepath.is_dir():
        bottom_dir_name = filepath.stem
        bottom_dir_name.strip().lower()
        if bottom_dir_name in IGNORE_DIR:
            return True
        for prefix in IGNORE_IF_STARTS:
            if bottom_dir_name.startswith(prefix):
                return True
    return False


def write_new_file(filepath: Path) -> None:
    """Creates a new file with the provided name and filepath"""
    create_directory(filepath)
    try:
        if filepath.is_file():
            raise FileExistsError(f"{filepath} already exists")
        with open(filepath, "w", encoding=UTF_8) as file:
            pass
    except FileNotFoundError:
        raise FileNotFoundError(f"{filepath} did not exists")


def save_filesnames_to_textfile(filepath_list):
    with open(CWD.joinpath("filenames.txt",), "w", encoding=UTF_8) as file:
        filepath_list = [str(filepath)+NEWLINE for filepath in filepath_list]
        file.writelines(filepath_list)


def read_file_names(filepath: Path) -> list[Path]:
    """"""
    filepath_list = list()
    with open(filepath, "r", encoding=UTF_8)as file:
        for filename in file:
            filepath_list.append(filename)
    return filepath_list


def get_rar_files(file_list: list[Path]) -> list[Path]:
    """Gets a list of all files with the extension '.rar.' """
    rar_list = list()
    for filepath in file_list:
        if filepath.suffix == ".rar":
            rar_list.append(filepath)
    return rar_list

def cleanup_rar_file(rar_file:FoundRarFile):
    """Cleans up the files associated with the rar file"""
    for file in rar_file.cleanup_files:
        delete_file(file)

def get_all_rar_files_in_tree(filepath: Path|str) -> list[Path]:
    """Gets a list of all files with the extension '.rar.' """
    file_list = get_all_filesnames_in_tree(Path(filepath))
    return get_rar_files(file_list)

def get_all_found_rar_files_in_tree(filepath: Path|str) -> list[FoundRarFile]:
    """Gets a list of all files with the extension '.rar.' """
    rar_files = get_all_rar_files_in_tree(Path(filepath))
    found_rar_files = list()
    for rar_file in rar_files:
        cleanup_files = find_cleanup_files(rar_file)
        video_file = find_extracted_file(rar_file)
        found_rar_files.append(FoundRarFile(rar_file, cleanup_files, video_file))

    return found_rar_files

def find_cleanup_files(filepath: Path) -> list[Path]:
    """Finds all files to be deleted"""
    delete_extensions = [".rar", ".sh"]
    cleanup_files = list()
    scriptfolder = filepath.parent
    folderfiles = get_all_directory_filenames(scriptfolder)
    for folderfile in folderfiles:
        if filepath.stem in str(folderfile):
            if folderfile.suffix in delete_extensions:
                cleanup_files.append(folderfile)
            elif is_multi_rar_extension(folderfile.suffix):
                cleanup_files.append(folderfile)
    return cleanup_files

def find_extracted_file(filepath: Path) -> str:
    """Finds the extracted file"""
    scriptfolder = filepath.parent
    folderfiles = get_all_directory_filenames(scriptfolder)
    for folderfile in folderfiles:
        filepath_name = (filepath.stem).lower()
        folderfile_name = (folderfile.stem).lower()
        if filepath_name in folderfile_name:
            extension = folderfile.suffix.lstrip(".").lower()
            if extension in VIDEO_EXTENSIONS:
                return folderfile.name
    return ""


def delete_file(filepath: Path) -> None:
    """Deletes the file provided"""
    os.remove(str(filepath))
