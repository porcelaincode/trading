from enum import Enum


class PositionEvents(Enum):
    CLOSE = 'close',
    UPDATE = 'update'


class PositionStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
