from fastapi import APIRouter
from starlette import status

from core.enums import ResultEnum
from core.response import default_responses, response_201, response_403, response_404, response_409, response_416
from repository.bid_request import BidRequestRepo
from repository.session import SessionRepo
from schemas.bid_request import BidRequestSchema

from .model import BidResponseModel, CreateBidRequestModel, NotifiedWinnerModel, WinningNotifiedResponseModel

router = APIRouter(prefix='/bid-requests', tags=['Bid Request'], responses=default_responses)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=BidResponseModel,
    responses={
        **response_409(),
        **response_403(),
        **response_416(),
        **response_404('session'),
        **response_201(BidRequestSchema, 'Bid Request')
    }
)
async def acquire_impressions(data: CreateBidRequestModel) -> BidResponseModel:
    BidRequestRepo.check_bid_request_is_duplicated(bid_request_id=data.request_id)
    session = SessionRepo.get_session(exchange_session_id=data.session_id)
    SessionRepo.check_session_status_is_valid(session=session)
    user = BidRequestRepo.get_user(user_id=data.user_id)
    bidding_price = BidRequestRepo.get_bidding_price(session=session, floor_price=data.floor_price, user=user)
    if bidding_price:
        bid_request = BidRequestRepo.create_bid_request(bid_request_data=data, bidding_price=bidding_price)
        return BidRequestRepo.convert_bidding_response_to_model(bid_request=bid_request)


@router.post(
    '/win-notified',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=WinningNotifiedResponseModel,
    responses={
        **response_404('session or bid Request'),
        **response_416(),
        **response_403()
    }
)
async def result_notification(data: NotifiedWinnerModel) -> WinningNotifiedResponseModel:
    session = SessionRepo.get_session(exchange_session_id=data.session_id)
    SessionRepo.check_session_status_is_valid(session=session)
    BidRequestRepo.check_bid_request_is_existed(bid_request_id=data.request_id)
    session_update_data = BidRequestRepo.get_acquired_session_and_used_budget(
        session=session, winning_price=data.clear_price
    )
    session = SessionRepo.update_session(session=session, update_data=session_update_data)
    return WinningNotifiedResponseModel(result=ResultEnum.ALLOWED)
