from fastapi import HTTPException, status

from domain.schema.survey_schema import DomainResSurveyResult, RouteReqPostSurvey, RouteResPostSurvey

import csv

def load_weights_from_csv(csv_path: str) -> list[list[float]]:

    weights = []
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            left_val = float(row['left'])
            center_val = float(row['center'])
            right_val = float(row['right'])
            weights.append([left_val, center_val, right_val])
    return weights


async def service_create_survey(
    data: RouteReqPostSurvey
) -> RouteResPostSurvey:
    try:
        weights = load_weights_from_csv('question_list.csv')
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


