from pydantic import BaseModel, Field


class RouteReqPostTopic(BaseModel):
    progressive: float = Field(title="진보 수치", ge=0, le=100, example=0)
    moderate: float = Field(title="중도 수치", ge=0, le=100, example=0)
    conservative: float = Field(title="보수 수치", ge=0, le=100, example=0)
    query: str = Field(title="검색어")


class RouteResPostTopic(BaseModel):
    articles: list[str] = Field(title="The articles")
    count: int = Field(title="The count of articles", ge=0)
