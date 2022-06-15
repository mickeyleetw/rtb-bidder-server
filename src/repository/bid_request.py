from collections import defaultdict
from decimal import Decimal

from apps.bid_request.model import BidResponseModel, CreateBidRequestModel
from apps.session.model import UpdateSessionModel
from core.exception import CPMValueNotAcceptableException, DuplicateRecordException, RangeExceedLimitException, \
    ResourceNotFoundException
from repository.session import ACCEPTABLE_CPM
from schemas.bid_request import BidRequestSchema, UserSchema
from schemas.session import SessionSchema

bid_request_map: dict[str, BidRequestSchema] = defaultdict()
user_map: dict[str, UserSchema] = defaultdict()


class BidRequestRepo:

    @staticmethod
    def get_user(user_id: str):
        return user_map.get(user_id, None)

    @staticmethod
    def check_bid_request_is_existed(bid_request_id: str):
        bid_request = bid_request_map.get(bid_request_id, None)
        if not bid_request:
            raise ResourceNotFoundException('bid request')

    @staticmethod
    def check_bid_request_is_duplicated(bid_request_id: str) -> bool:
        bid_request = bid_request_map.get(bid_request_id, None)
        if bid_request:
            raise DuplicateRecordException('bid request')

    @staticmethod
    def get_bidding_price(session: SessionSchema, floor_price: Decimal, user: UserSchema = None):
        if user is not None:
            target_impression = user.real_impression - session.impression_acquired
        target_impression = session.exchange_session.impression_goal - session.impression_acquired
        if target_impression <= 0:
            raise RangeExceedLimitException('impression amount')
        else:
            target_price = session.exchange_session.budget - session.budget_used
            bidding_price = (ACCEPTABLE_CPM / 1000) * target_impression
            if bidding_price < floor_price:
                raise CPMValueNotAcceptableException()
            if bidding_price > target_price:
                bidding_price = target_price
                # raise RangeExceedLimitException('budget')
        return bidding_price

    @staticmethod
    def create_bid_request(bid_request_data: CreateBidRequestModel, bidding_price: Decimal) -> BidRequestSchema:
        data = BidRequestSchema(
            request_id=bid_request_data.request_id,
            session_id=bid_request_data.session_id,
            user_id=bid_request_data.user_id,
            floor_price=bid_request_data.floor_price,
            bidding_price=bidding_price
        )
        # use request_id as key
        bid_request_map[bid_request_data.request_id] = data
        return data

    @staticmethod
    def convert_bidding_response_to_model(bid_request: BidRequestSchema):
        return BidResponseModel(
            session_id=bid_request.session_id, request_id=bid_request.request_id, price=bid_request.bidding_price
        )

    @staticmethod
    def get_acquired_session_and_used_budget(session: SessionSchema, winning_price: Decimal) -> dict:
        session_cpm = (session.exchange_session.budget / session.exchange_session.impression_goal) * 10000
        impression_get = (winning_price * 1000) / session_cpm
        budget_used = session.exchange_session.budget - winning_price
        if budget_used < 0:
            raise RangeExceedLimitException('budget')
        update_data = UpdateSessionModel(impression_acquired=impression_get, budget_used=budget_used)
        return update_data
