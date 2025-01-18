import requests
import asyncio
import aiohttp

import json
import re

import csv
import pandas as pd

# 1에 가까울수록 진보, 10에에 

press_dict = {
    "018": "이데일리",
    "088": "매일신문",
    "214": "MBC",
    "015": "한국경제",
    "052": "YTN",
    "008": "머니투데이",
    "032": "경향신문",
    "366": "조선비즈",
    "005": "국민일보",
    "023": "조선일보",
    "081": "서울신문",
    "025": "중앙일보",
    "087": "강원일보",
    "469": "한국일보",
    "006": "미디어오늘",
    "421": "뉴스1",
    "001": "연합뉴스",
    "422": "연합뉴스TV",
    "437": "JTBC",
    "011": "서울경제",
    "057": "MBN",
    "055": "SBS",
    "031": "아이뉴스24",
    "021": "문화일보",
    "119": "데일리안",
    "053": "주간조선",
    "296": "코메디닷컴",
    "009": "매일경제",
    "028": "한겨레",
    "016": "헤럴드경제",
    "014": "파이낸셜뉴스",
    "056": "KBS",
    "047": "오마이뉴스",
    "584": "동아사이언스",
    "079": "노컷뉴스",
    "449": "채널A",
    "277": "아시아경제",
    "022": "세계일보",
    "020": "동아일보",
    "648": "비즈워치",
    "629": "더팩트",
    "346": "헬스조선",
    "082": "부산일보",
    "123": "조세일보",
    "029": "디지털타임스",
    "607": "뉴스타파",
    "660": "kbc광주방송",
    "003": "뉴시스",
    "374": "SBS Biz",
    "215": "한국경제TV",
    "293": "블로터",
    "586": "시사저널",
    "030": "전자신문",
    "448": "TV조선",
    "138": "디지털데일리",
    "092": "지디넷코리아",
    "262": "신동아",
    "044": "코리아헤럴드",
    "127": "기자협회보",
    "662": "농민신문",
    "002": "프레시안",
    "050": "한경비즈니스",
    "666": "경기일보",
    "654": "강원도민일보",
    "094": "월간 산",
    "656": "대전일보",
    "024": "매경이코노미",
    "658": "국제신문",
    "308": "시사IN",
    "640": "코리아중앙데일리",
    "243": "이코노미스트",
    "417": "머니S",
    "310": "여성신문",
    "659": "전주MBC",
    "036": "한겨레21",
    "661": "JIBS",
    "033": "주간경향",
    "007": "일다",
    "657": "대구MBC",
    "037": "주간동아",
    "655": "CJB청주방송",
    "665": "더스쿠프",
    "353": "중앙SUNDAY",
    "145": "레이디경향"
}


# 네이버 API 인증 정보
CLIENT_ID = "bAH1YsUVJACd04LZpvmx"  # 발급받은 클라이언트 ID
CLIENT_SECRET = "QRde3I7aiD"  # 발급받은 클라이언트 시크릿


async def fetch_naver_news(session, query, display=50, start=1, sort="date"):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort,
    }

    async with session.get(url, headers=headers, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error Code: {response.status}")
            return None


# URL에서 언론사 ID 추출 함수
def find_office_id(url):
    match = re.search(r'/article/(\d+)/', url)
    if match:
        office_id = match.group(1)
        return press_dict.get(office_id, "")
    return None


# 뉴스 링크 가져오기
async def query_naver_links(query):
    async with aiohttp.ClientSession() as session:
        news_data = await fetch_naver_news(session, query)

        if not news_data:
            print("No data fetched.")
            return [], [], []

        urls, descriptions, titles = [], [], []

        for item in news_data.get("items", []):
            urls.append(item["link"])
            descriptions.append(item["description"])
            titles.append(item["title"])

        return urls, descriptions, titles

'''
# asyncio 실행
if __name__ == "__main__":
    asyncio.run(main())
'''