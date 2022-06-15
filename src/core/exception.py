from fastapi import status

from core.enums import ErrorCode


class BaseException_(Exception):
    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = ErrorCode.GENERAL_1001_UNEXPECTED_ERROR
    message = 'Unexpected'

    def __init__(self, msg=None, **kwargs):
        if not msg:
            msg = self.message
        for k, v in kwargs.items():
            setattr(self, k, v)

        super().__init__(msg)


class ResourceNotFoundException(BaseException_):

    def __init__(self, subject: str):
        super().__init__(
            code=ErrorCode.GENERAL_1006_RESOURCE_NOT_FOUND,
            http_status=status.HTTP_404_NOT_FOUND,
            message=f'{subject} not found'
        )


class InvalidStateTransitionException(BaseException_):

    def __init__(self):
        super().__init__(
            code=ErrorCode.GENERAL_1003_INVALID_STATE_TRANSITION,
            http_status=status.HTTP_403_FORBIDDEN,
            message='state error'
        )


class DuplicateRecordException(BaseException_):

    def __init__(self, subject: str):
        super().__init__(
            code=ErrorCode.GENERAL_1004_DUPLICATE_RECORD,
            http_status=status.HTTP_409_CONFLICT,
            message=f'{subject} is duplicate'
        )


class RangeExceedLimitException(BaseException_):

    def __init__(self, subject: str):
        super().__init__(
            code=ErrorCode.GENERAL_1005_IMPRESSION_EXCEED_LIMIT,
            http_status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            message=f'{subject} exceeded limit'
        )


class CPMValueNotAcceptableException(BaseException_):

    def __init__(self):
        super().__init__(
            code=ErrorCode.GENERAL_1007_CPM_VALUE_NOT_ACCEPTABLE,
            http_status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            message='CPM value not acceptable'
        )
