from fastapi import HTTPException, status

from domain.schema.survey_schema import DomainResSurveyResult, RouteReqPostSurvey, RouteResPostSurvey


async def service_create_survey(
    data: RouteReqPostSurvey
) -> RouteResPostSurvey:
    try:
        weights = [[0.549, 0.144, 0.307], [0.601, 0.200, 0.199], [0.300, 0.400, 0.300]]
        left, center, right = 0, 0, 0
        for answer, weight in zip(data.answers, weights):
            left += answer * weight[0]
            center += answer * weight[1]
            right += answer * weight[2]
        total = left + center + right

        left_percentage = (left/total) * 100
        center_percentage = (center/total) * 100
        right_percentage = (right/total) * 100

        res = DomainResSurveyResult(
            progressive=left_percentage,
            moderate=center_percentage,
            conservative=right_percentage,
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
