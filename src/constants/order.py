from enum import Enum


class OrderEvents(Enum):
    CANCEL = 'cancel'


class OrderStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    CANCELLED = 'cancelled'
    PENDING = 'pending'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
