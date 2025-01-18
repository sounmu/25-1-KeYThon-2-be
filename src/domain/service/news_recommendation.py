import asyncio

from naverNews import fetch_naver_news, find_office_id, query_naver_links


async def naver_main():
    query = "대통령"
    print(f"Query: {query}")

    urls, descriptions, titles = await query_naver_links(query)
    office_ids = [find_office_id(url) for url in urls]

    # 언론사 정보 출력
    for url, office_id in zip(urls, office_ids):
        print(f"URL: {url}")
        print(f"언론사: {office_id}")

    return urls, descriptions, titles



# asyncio 실행
if __name__ == "__main__":
    asyncio.run(naver_main())