from typing import Union

from fastapi import APIRouter

from core.response import default_responses, response_404,response_201
from starlette import status

from .model import RetrieveBidResultModel,CreateBidRequestModel

router = APIRouter(prefix='/bid-requests', tags=['Bid Request'], responses=default_responses)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=RetrieveBidResultModel,
    responses={
        **response_404('Bid Request'),
        **response_201(RetrieveBidResultModel,'Bid Request')
    }
)
async def acquire_impressions(data:CreateBidRequestModel) -> RetrieveBidResultModel:
    # TODO: to be implemented
    pass

@router.post(
    '/winning-notified',
    status_code=status.HTTP_201_CREATED,
    response_model=RetrieveBidResultModel,
    responses={
        **response_404('Bid Request'),
        **response_201(RetrieveBidResultModel,'Bid Request')
    }
)
async def acquire_impressions(data:CreateBidRequestModel) -> RetrieveBidResultModel:
    # TODO: to be implemented
    pass
