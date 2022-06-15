import enum


@enum.unique
class ErrorCode(enum.IntEnum):
    GENERAL_1001_UNEXPECTED_ERROR = 1001
    GENERAL_1002_REQUEST_VALIDATION_FAILED = 1002
    GENERAL_1003_INVALID_STATE_TRANSITION = 1003
    GENERAL_1004_DUPLICATE_RECORD = 1004
    GENERAL_1005_IMPRESSION_EXCEED_LIMIT = 1005
    GENERAL_1006_RESOURCE_NOT_FOUND = 1006
    GENERAL_1007_CPM_VALUE_NOT_ACCEPTABLE = 1007


class StrEnum(str, enum.Enum):
    pass


class ResultEnum(StrEnum):
    ALLOWED = 'ok'
    DENIED = 'no'


class SessionStatusEnum(StrEnum):
    OPENED = 'opened'
    UNKNOWN = 'unknown'
    CLOSED = 'closed'
