from typing import Type

from pydantic import BaseModel
from starlette import status

from core.enums import ErrorCode


class ErrorMessage(BaseModel):
    code: int
    message: str


default_responses: dict = {
    status.HTTP_422_UNPROCESSABLE_ENTITY:
        {
            'model': ErrorMessage,
            'description': 'Validation error',
            'content':
                {
                    'application/json':
                        {
                            'example':
                                {
                                    'code': ErrorCode.GENERAL_1002_REQUEST_VALIDATION_FAILED,
                                    'message': 'validation error'
                                }
                        }
                },
        },
    status.HTTP_500_INTERNAL_SERVER_ERROR:
        {
            'model': ErrorMessage,
            'description': 'Internal error',
            'content':
                {
                    'application/json':
                        {
                            'example': {
                                'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR,
                                'message': 'internal error'
                            }
                        }
                },
        }
}


def response_201(model: Type[BaseModel], subject: str) -> dict:
    return {status.HTTP_201_CREATED: {'model': model, 'description': f'{subject} has been created'}}


def response_404(subject: str) -> dict:
    return {
        status.HTTP_404_NOT_FOUND:
            {
                'model': ErrorMessage,
                'description': f'{subject} not found',
                'content':
                    {
                        'application/json':
                            {
                                'example':
                                    {
                                        'code': ErrorCode.GENERAL_1006_RESOURCE_NOT_FOUND,
                                        'message': 'resource not found'
                                    }
                            }
                    },
            }
    }


def response_400() -> dict:
    return {status.HTTP_400_BAD_REQUEST: {'model': ErrorMessage, 'description': 'Bidder API unexpected error'}}


def response_403() -> dict:
    return {
        status.HTTP_403_FORBIDDEN:
            {
                'model': ErrorMessage,
                'description': 'Forbidden',
                'content':
                    {
                        'application/json':
                            {
                                'example':
                                    {
                                        'code': ErrorCode.GENERAL_1003_INVALID_STATE_TRANSITION,
                                        'message': 'state error'
                                    }
                            }
                    }
            }
    }


def response_409() -> dict:
    return {status.HTTP_409_CONFLICT: {'model': ErrorMessage, 'description': 'Conflict'}}


def response_416() -> dict:
    return {
        status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: {
            'model': ErrorMessage,
            'description': 'not to participate'
        }
    }
