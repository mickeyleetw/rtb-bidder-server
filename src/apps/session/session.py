from fastapi import APIRouter

from apps.session.model import EndSessionModel, InitSessionModel, SessionResponseModel, UpdateSessionModel
from core.enums import ResultEnum, SessionStatusEnum
from core.response import default_responses, response_201, response_403, response_404, response_409
from repository.session import SessionRepo
from schemas.session import SessionSchema

router = APIRouter(prefix='/sessions', tags=['Session'], responses=default_responses)


@router.post(
    '/init',
    response_model=SessionResponseModel,
    responses={
        **response_201(SessionSchema, 'Session'),
        **response_409()
    }
)
async def init_session(data: InitSessionModel) -> SessionResponseModel:
    SessionRepo.check_session_is_duplicated(exchange_session_id=data.session_id)
    is_cpm_acceptable = SessionRepo.check_budget_impression_ratio_is_acceptable(
        budget=data.budget, impression_goal=data.impression_goal
    )
    is_cpc_acceptable = SessionRepo.check_budget_traffic_ratio_is_acceptable(
        budget=data.budget, estimated_traffic=data.estimated_traffic
    )
    if is_cpc_acceptable and is_cpm_acceptable:
        result = ResultEnum.ALLOWED
        new_session = SessionRepo.create_session(session_data=data)
    else:
        result = ResultEnum.DENIED
        new_session = None
    return SessionRepo.convert_session_response_to_model(session=new_session, result=result)


@router.post(
    '/end', response_model=SessionResponseModel, responses={
        **response_404('Session'),
        **response_403(),
    }
)
async def end_session(data: EndSessionModel) -> SessionResponseModel:
    session = SessionRepo.get_session(exchange_session_id=data.session_id)
    SessionRepo.check_session_status_is_valid(session=session)
    update_data = UpdateSessionModel(status=SessionStatusEnum.CLOSED)
    session = SessionRepo.update_session(session=session, update_data=update_data)
    result = ResultEnum.ALLOWED
    return SessionRepo.convert_session_response_to_model(session=session, result=result)
