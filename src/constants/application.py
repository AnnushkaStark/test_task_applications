import enum

MIN_APPLICATION_NAME_LENGTH = 2
MAX_APPLICATION_NAME_LENGTH = 100

MIN_APPLICATION_TEXT_LENGTH = 2
MAX_APPLICATION_TEXT_LENGTH = 1000


class ApplicationStatus(enum.StrEnum):
    OPEN = "Open"
    IN_PROGRESS = "In progress"
    COMPLITED = "Complited"
