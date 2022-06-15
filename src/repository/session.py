import decimal
from collections import defaultdict
from decimal import Decimal

from apps.session.model import InitSessionModel, SessionResponseModel
from core.enums import ResultEnum, SessionStatusEnum
from core.exception import DuplicateRecordException, InvalidStateTransitionException, ResourceNotFoundException
from schemas.session import ExchangeSessionSchema, SessionSchema

decimal.Context(prec=2)
# session_map  here to be used as RDBS
session_map: dict[str, SessionSchema] = defaultdict()

# use common CPM & CPC value to accept the bidding or not
# CPM & CPC might be provided from Data or ML engineer or
# bidder-server should calculate these values in background job
# cost per thousand impression (CPM = budget/(1000*impression))
ACCEPTABLE_CPM = Decimal(150)

# cost per click (CPC =budget/estimated_traffic)
ACCEPTABLE_CPC = Decimal(5)


class SessionRepo:

    @staticmethod
    def check_session_is_duplicated(exchange_session_id: str) -> bool:
        session = session_map.get(exchange_session_id, None)
        if session and session.status == SessionStatusEnum.OPENED:
            raise DuplicateRecordException('session')
        # NOTE: not sure if session can be repeatably created with same session id
        elif session and session.status == SessionStatusEnum.CLOSED:
            raise DuplicateRecordException('session with same id')

    @staticmethod
    def check_budget_impression_ratio_is_acceptable(budget: Decimal, impression_goal: int) -> bool:
        if (budget / Decimal(impression_goal / 1000)) <= ACCEPTABLE_CPM:
            return True
        else:
            return False

    @staticmethod
    def check_budget_traffic_ratio_is_acceptable(budget: Decimal, estimated_traffic: int) -> bool:
        if (budget / estimated_traffic) <= ACCEPTABLE_CPC:
            return True
        else:
            return False

    @staticmethod
    def convert_session_info_to_exchange_session_schema(
        exchange_session_data: InitSessionModel
    ) -> ExchangeSessionSchema:
        exchange_data = ExchangeSessionSchema(
            session_id=exchange_session_data.session_id,
            estimated_traffic=exchange_session_data.estimated_traffic,
            budget=exchange_session_data.budget,
            impression_goal=exchange_session_data.impression_goal
        )
        return exchange_data

    @staticmethod
    def create_session(session_data: InitSessionModel) -> SessionSchema:
        data = SessionSchema(
            status=SessionStatusEnum.OPENED,
            exchange_session=SessionRepo.convert_session_info_to_exchange_session_schema(
                exchange_session_data=session_data
            )
        )
        # use exchange session_id as key
        session_map[session_data.session_id] = data
        return data

    @staticmethod
    def convert_session_response_to_model(result: ResultEnum, session: SessionSchema = None):
        if session:
            return SessionResponseModel(
                status=session.status, exchange_session_id=session.exchange_session.session_id, result=result
            )
        else:
            return SessionResponseModel(result=result)

    @staticmethod
    def get_session(exchange_session_id: str) -> SessionSchema:
        session = session_map.get(exchange_session_id, None)
        if not session:
            raise ResourceNotFoundException('Session')
        return session

    @staticmethod
    def check_session_status_is_valid(session: SessionSchema):
        if session.status != SessionStatusEnum.OPENED:
            raise InvalidStateTransitionException()

    @staticmethod
    def update_session(session: SessionSchema, update_data: dict = None) -> SessionSchema:
        data_dict = session.dict()
        if update_data != {}:
            for key, val in update_data.dict(exclude_unset=True).items():
                data_dict[key] = val
        return SessionSchema(**data_dict)
