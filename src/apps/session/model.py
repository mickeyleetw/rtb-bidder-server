import decimal
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from core.enums import ResultEnum, SessionStatusEnum

decimal.Context(prec=2)


class BidderModel(BaseModel):
    name: str
    endpoint: str


class BidderRequirementModel(BaseModel):
    budget: Decimal = Field(gt=0)
    impression_goal: int = Field(gt=0)


class InitSessionModel(BidderRequirementModel):
    session_id: str
    estimated_traffic: int = Field(gt=0)


class EndSessionModel(BaseModel):
    session_id: str


class UpdateSessionModel(BaseModel):
    status: Optional[SessionStatusEnum]
    impression_acquired: Optional[int]
    budget_used: Optional[Decimal]


class SessionResponseModel(BaseModel):
    status: Optional[SessionStatusEnum]
    exchange_session_id: Optional[str]
    result: ResultEnum
