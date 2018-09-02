from enum import Enum


class CheckErrorLevel(Enum):
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3


class CheckError(Exception):
    def __init__(self, level: CheckErrorLevel, message: str):
        self.level = level
        self.message = message
