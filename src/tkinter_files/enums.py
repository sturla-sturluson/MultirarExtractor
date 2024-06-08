from enum import Enum, auto
# Enums for the buttons
class Size(Enum):
    FIT = auto() # For auto width buttons
    XSMALL = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    XLARGE = auto()


class Variant(Enum):
    PRIMARY = auto()
    SECONDARY = auto()
    TERTIARY = auto()
    SUCCESS = auto()
    WARNING = auto()
    DANGER = auto()
    INFO = auto()
    LIGHT = auto()
    DARK = auto()

class Enabled(Enum):
    ENABLED = auto()
    DISABLED = auto()

class Action(Enum):
    SEARCH = auto()
    DELETE = auto()
    DELETE_EXTRACTED = auto()
    EXTRACT = auto()
    EXECUTE = auto()