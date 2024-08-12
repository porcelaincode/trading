from enum import Enum


class AppEvents(Enum):
    INSTRUCTION = 'instruction'


class AppInstructions(Enum):
    START = 'START'
    STOP = 'STOP'
