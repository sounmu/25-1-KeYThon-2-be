from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from domain.schema.survey_schema import RouteReqPostSurvey, RouteResPostSurvey
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


@router.get("/")
async def read_root():
    return {"message": "Hello World"}
