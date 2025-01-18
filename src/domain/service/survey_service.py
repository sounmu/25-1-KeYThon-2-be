from fastapi import HTTPException, status

from domain.schema.survey_schema import RouteReqPostSurvey, RouteResPostSurvey


async def service_create_survey(
    data: RouteReqPostSurvey
) -> RouteResPostSurvey:
    try:
        score = 0
        for i in range(20):
            answer = data.answers[str(i)]
            options = ["강하게 동의", "다소 동의", "약간 동의", "약간 비동의", "다소 비동의", "강하게 비동의"]

            if i % 2 == 1:  # 홀수
                score += options.index(answer)
            else:  # 짝수
                score += 5 - options.index(answer)

        response = RouteResPostSurvey(
            result=score
        )

    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
