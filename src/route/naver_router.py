from typing import Annotated

from fastapi import APIRouter, Body, status

from domain.schema.survey_schema import RouteReqPostSurvey, RouteResPostSurvey
from domain.schema.topic_schema import RouteReqPostTopic, RouteResPostTopic
from domain.service.survey_service import service_create_survey

router = APIRouter(
    prefix="/api/naver",
    tags=["api"],
)


@router.post("/query",
    summary="네이버 뉴스 쿼리로 검색색",
    response_model=RouteResPostSurvey,
    status_code=status.HTTP_200_OK,
)
async def 