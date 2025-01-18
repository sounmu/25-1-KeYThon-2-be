from pydantic import BaseModel, Field


class RouteReqPostTopic(BaseModel):
    point: int = Field(title="The point", ge=0, le=100)
    topic: str = Field(title="The topic")


class RouteResPostTopic(BaseModel):
    articles: list[str] = Field(title="The articles")
    count: int = Field(title="The count of articles", ge=0)
