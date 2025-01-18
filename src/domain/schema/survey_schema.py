from typing import Dict

from pydantic import BaseModel, Field, validator


class RouteReqPostSurvey(BaseModel):
    answers: list[int] = Field(title="The survey answers")


class RouteResPostSurvey(BaseModel):
    progressive: float = Field(title="진보", example=33.33) # 소수점 둘째 자리까지, 자동 반올림
    moderate: float = Field(title="진보", example=33.33)
    conservative: float = Field(title="진보", example=33.33)

    @validator("progressive", "moderate", "conservative", pre=True)
    def round_to_two_decimal_places(cls, value):
        return round(value, 2)


class RouteReqPostTopic(BaseModel):
    point: int = Field(title="The point", ge=0, le=100)
    topic: str = Field(title="The topic")


class RouteResPostTopic(BaseModel):
    articles: Dict[str, str] = Field(title="The articles")
    count: int = Field(title="The count of articles", ge=0)
