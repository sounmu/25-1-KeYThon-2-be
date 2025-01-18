from domain.schema.topic_schema import RouteReqPostTopic, RouteResPostTopic
from domain.service.news_recommendation import user_polar_result


async def service_create_topic(
    data: RouteReqPostTopic,
) -> RouteResPostTopic:
    polar = [data.progressive, data.moderate, data.conservative]
    query = data.query

    data, count = await user_polar_result(polar, query)

    response = RouteResPostTopic(
        data=data,
        count=count
    )

    return response
