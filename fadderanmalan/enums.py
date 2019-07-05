from enum import Enum


class ActionTypes(Enum):
    REGISTRATION_CREATE = "Create registration"
    REGISTRATION_DELETE = "Delete registration"

    ENTER_QUEUE_CREATE = "Create enter queue"
    ENTER_QUEUE_DELETE = "Delete enter queue"

    LEAVE_QUEUE_CREATE = "Create leave queue"
    LEAVE_QUEUE_DELETE = "Delete leave queue"
