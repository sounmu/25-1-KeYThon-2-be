from pydantic import BaseModel, Field


class RouteReqPostTopic(BaseModel):
    progressive: float = Field(title="吏꾨낫 �닔移�", ge=0, le=100, example=0)
    moderate: float = Field(title="以묐룄 �닔移�", ge=0, le=100, example=0)
    conservative: float = Field(title="蹂댁닔 �닔移�", ge=0, le=100, example=0)
    query: str = Field(title="寃��깋�뼱")


class DomainResPostTopic(BaseModel):
    title: str # �젣紐�
    descriptions : str # �슂�빟
    office : str # �뼵濡좎궗
    url : str # �돱�뒪 留곹겕
    bias : str # �젙移� �꽦�뼢


class RouteResPostTopic(BaseModel):
    data: list[DomainResPostTopic] = Field(title="The articles")
    count: int = Field(title="The count of articles", ge=0)

