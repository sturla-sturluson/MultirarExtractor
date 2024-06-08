from dataclasses import dataclass
from pathlib import Path
from ..enums import Action


@dataclass
class SavedPath:
    path:str|Path
    toggled:bool

    # Serialization

    def __dict__(self):
        return {
            "path": str(self.path),
            "toggled": self.toggled
        }
            
@dataclass
class ActionButton:
    action:Action
    toggled:bool

@dataclass
class FoundRarFile:
    path:Path # This is the top level rar file, the one that ends with .rar
    cleanup_files:list[Path] # These are all the files that need to be deleted after extraction
    extracted_filename:str = "" # The extension of the extracted file, if it has been extracted
    is_extracting:bool = False # If the file is currently being extracted
    

    @property
    def extracted(self):
        return self.extracted_filename != ""

    @property
    def extracted_name(self):
        return self.extracted_filename