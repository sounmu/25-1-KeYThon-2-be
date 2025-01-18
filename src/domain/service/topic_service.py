from fastapi import HTTPException, status

from domain.schema.topic_schema import RouteReqPostTopic, RouteResPostTopic


async def service_create_topic(
    data: RouteReqPostTopic
) -> RouteResPostTopic:
    pass
