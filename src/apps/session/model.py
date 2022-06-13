from decimal import Decimal

from pydantic import BaseModel

from core.enums import ResultEnum


class BidderModel(BaseModel):
    name: str
    endpoint: str


class BidderRequirementModel(BaseModel):
    budget: Decimal
    impression_goal: int


class InitSessionModel(BaseModel):
    session_id: str
    estimated_traffic: int
    budget:Decimal
    impression_goal:int


class EndSessionModel(BaseModel):
    session_id: str


class SessionResponseModel(BaseModel):
    result: ResultEnum
