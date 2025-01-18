from pydantic import BaseModel, Field
from typing import Dict

class RouteReqPostTopic(BaseModel):
    progressive: float = Field(title="진보 수치", ge=0, le=100, example=0)
    moderate: float = Field(title="중도 수치", ge=0, le=100, example=0)
    conservative: float = Field(title="보수 수치", ge=0, le=100, example=0)
    query: str = Field(title="검색어")


class DomainResPostTopic(BaseModel):
    title: str # 제목
    descriptions : str # 요약
    office : str # 언론사
    url : str # 뉴스 링크
    bias : str # 정치 성향


class RouteResPostTopic(BaseModel):
    data: list[DomainResPostTopic] = Field(title="The articles")
    count: int = Field(title="The count of articles", ge=0)

