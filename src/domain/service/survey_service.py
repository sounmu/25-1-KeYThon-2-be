from fastapi import HTTPException, status

from domain.schema.survey_schema import DomainResSurveyResult, RouteReqPostSurvey, RouteResPostSurvey


async def service_create_survey(
    data: RouteReqPostSurvey
) -> RouteResPostSurvey:
    try:
        score = 0
        for i in range(20):
            answer = data.answers[i]
            # 새로운 로직 필요
            score += answer

        res = DomainResSurveyResult(
            progressive=score,
            moderate=score,
            conservative=score,
        )

        response = RouteResPostSurvey(
            result=res,
        )

    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
