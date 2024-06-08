from pathlib import Path


SCRIPT_PREFIX = "script_"


def create_script_file(filepath: Path, script_command: str) -> Path:
    """Creates a .sh script file"""
    filepath = filepath.parent.joinpath(SCRIPT_PREFIX + filepath.stem + ".sh")

    with open(filepath, "w") as file:
        file.write(script_command)

    return filepath


def create_7z_extract_script(filepath: Path) -> Path:
    """Creates a 7zip extract script for the provided filepath
        Returns the script path"""
    # Getting the command to extract the file
    script_cmd = get_script_command(filepath)
    # Creating the script file which can be run later
    script_path = create_script_file(filepath, script_cmd)
    return script_path

def get_script_command(filepath: Path) -> str:
    """Gets a 7zip extract console command
    Example: 7z x "C://Users//user//Downloads//file.rar" -o"C://Users//user//Downloads//"
    """
    _safe_filepath = str(filepath).replace("\\", "//")
    _safe_parent = str(filepath.parent).replace("\\", "//")

    return f"7z x \"{_safe_filepath}\" -o\"{_safe_parent}\""