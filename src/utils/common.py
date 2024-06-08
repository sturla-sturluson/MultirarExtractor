from pathlib import Path
from ..constants import NEWLINE
import re


def get_shortened_path_name(path: str|Path) -> str:
    """Returns a shortened version of the path name
    The shortened version will be the root folder name and the last folder name
    Example: "C:/Users/username/Documents" -> "C:/.../Documents"
    """
    path = Path(path)
    first_part = str(path.parts[0]).replace("\\", "/")
    if(len(path.parts) == 1):
        return str(path.parts[0]).replace("\\", "/")
    last_part = str(path.parts[-1]).replace("\\", "/")
    if(len(path.parts) == 2):
        return f"{first_part}/.../{last_part}"
    second_part = str(path.parts[1]).replace("\\", "/")
    return f"{first_part}{second_part}/... /{last_part}"

def format_extracted_video_names(list_of_extracted_names: list[Path]):
    info_string = "Found Video Files: " + NEWLINE
    found = False
    for filename in list_of_extracted_names:
        found = True
        filestring = get_file_string(filename)

        info_string += filestring + NEWLINE
    if not found:
        info_string += "Nothing found!"
    return info_string

def get_file_string(filename: Path):
    """Returns a string with the name and size of the file"""
    filestring = f"Name: {str(filename.name)} "
    stats = filename.stat()
    filestring += f"Size: {format_size(stats.st_size)}"
    return filestring

def format_size(filesize: int) -> str:
    """Returns the filesize in correct format"""
    size_suffixes = ["b", "kb", "mb", "gb", "tb", "pb"]
    for suffix in size_suffixes:
        if filesize < 1024:
            break
        filesize //= 1024
    return f"{filesize:.2f}{suffix}"


def suffix_checker(suffix: str) -> str:
    """Strips and adds a dot before the extension"""
    suffix = suffix.lstrip(".")
    return f".{suffix}"

def is_multi_rar_extension(suffix: str) -> bool:
    """Returns true if the extension is .r00-r99"""
    suffix = suffix_checker(suffix)
    suffix_regex = r".r\d\d"
    search = re.match(suffix_regex, suffix)
    if search != None:
        return True
    return False


def get_plural_suffix(count: int, suffix:str) -> str:
    """Returns the correct suffix for the word file"""
    return "" if count == 1 else suffix

