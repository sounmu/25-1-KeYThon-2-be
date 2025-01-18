from typing import Annotated

from fastapi import APIRouter, Body, status

from domain.schema.survey_schema import RouteReqPostSurvey, RouteResPostSurvey
from domain.schema.topic_schema import RouteReqPostTopic, RouteResPostTopic
from domain.service.survey_service import service_create_survey

router = APIRouter(
    prefix="/api",
    tags=["api"],
)


@router.post(
    "/survey",
    summary="설문 작성",
    response_model=RouteResPostSurvey,
    status_code=status.HTTP_200_OK,
)
async def create_survey(
    survey: RouteReqPostSurvey,
) -> RouteResPostSurvey:
    result = await service_create_survey(survey)

    return result


@router.post(
    "/topic",
    summary="주제 입력",
    response_model=RouteResPostTopic,
    status_code=status.HTTP_200_OK,
)
async def create_topic(
    point: Annotated[int, Body(ge=0, le=100, description="The point")],
    topic: Annotated[str, Body(description="The topic")],
) -> RouteResPostTopic:
    result = await service_create_survey(
        RouteReqPostTopic(
            point=point,
            topic=topic,
        )
    )
    return result


@router.get("/")
async def read_root():
    return {"message": "Hello World"}
