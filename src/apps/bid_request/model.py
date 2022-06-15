import decimal
from decimal import Decimal

from pydantic import BaseModel, Field

from core.enums import ResultEnum

decimal.Context(prec=2)


class CreateBidRequestModel(BaseModel):
    floor_price: Decimal = Field(ge=0)
    timeout_ms: int
    session_id: str
    user_id: str
    request_id: str


class NotifiedWinnerModel(BaseModel):
    session_id: str
    request_id: str
    clear_price: Decimal


class WinningNotifiedResponseModel(BaseModel):
    result: ResultEnum


class BidResponseModel(BaseModel):
    session_id: str
    request_id: str
    price: Decimal
