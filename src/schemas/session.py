from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from core.enums import SessionStatusEnum


class ExchangeSessionSchema(BaseModel):
    session_id: Optional[str]
    estimated_traffic: int
    budget: Decimal
    impression_goal: int


class SessionSchema(BaseModel):
    status: SessionStatusEnum
    exchange_session: ExchangeSessionSchema
    impression_acquired: int = Field(default=0)
    budget_used: Decimal = Field(default=0)
