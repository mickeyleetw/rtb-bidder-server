from decimal import Decimal

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: str
    real_impression: int


class BidRequestSchema(BaseModel):
    request_id: str
    session_id: str
    user_id: str
    floor_price: Decimal
    bidding_price: Decimal
