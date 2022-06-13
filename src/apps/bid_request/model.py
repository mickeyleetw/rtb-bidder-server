from decimal import Decimal
from pydantic import BaseModel


class CreateBidRequestModel(BaseModel):
    floor_price: Decimal
    timeout:int
    session_id:str
    user_id:str
    request_id:str


class NotifiedWinnerModel(BaseModel):
    session_id:str
    request_id:str
    clear_price:Decimal


class RetrieveBidResultModel(BaseModel):
    session_id:str
    request_id:str
    price:Decimal


