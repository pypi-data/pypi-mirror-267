from enum import Enum

class ScriptType(Enum):
    TEXT = 1
    FILE = 2
    
ScriptType = Enum("ScriptType", ["TEXT", "FILE"])