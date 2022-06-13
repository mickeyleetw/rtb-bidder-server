import enum


@enum.unique
class ErrorCode(enum.IntEnum):
    GENERAL_1001_UNEXPECTED_ERROR = 1001
    GENERAL_1002_REQUEST_VALIDATION_FAILED = 1002
    GENERAL_1003_REQUEST_VALIDATION_FAILED = 1003

    RESOURCE_2001_NOT_FOUND = 2001


class StrEnum(str, enum.Enum):
    pass


class ResultEnum(StrEnum):
    ALLOWED = 'ok'
