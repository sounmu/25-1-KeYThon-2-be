import re

import aiohttp

# 1?�� �?까울?���? 진보, 10?�� �?까울?���? 보수

press_dict = {
    "018": "?��?��?���?",
    "088": "매일?���?",
    "214": "MBC",
    "015": "?���?경제",
    "052": "YTN",
    "008": "머니?��?��?��",
    "032": "경향?���?",
    "366": "조선비즈",
    "005": "�?민일�?",
    "023": "조선?���?",
    "081": "?��?��?���?",
    "025": "중앙?���?",
    "087": "강원?���?",
    "469": "?���??���?",
    "006": "미디?��?��?��",
    "421": "?��?��1",
    "001": "?��?��?��?��",
    "422": "?��?��?��?��TV",
    "437": "JTBC",
    "011": "?��?��경제",
    "057": "MBN",
    "055": "SBS",
    "031": "?��?��?��?��24",
    "021": "문화?���?",
    "119": "?��?��리안",
    "053": "주간조선",
    "296": "코메?��?���?",
    "009": "매일경제",
    "028": "?��겨레",
    "016": "?��?��?��경제",
    "014": "?��?��?��?��?��?��",
    "056": "KBS",
    "047": "?��마이?��?��",
    "584": "?��?��?��?��?��?��",
    "079": "?��컷뉴?��",
    "449": "채널A",
    "277": "?��?��?��경제",
    "022": "?��계일�?",
    "020": "?��?��?���?",
    "648": "비즈?���?",
    "629": "?��?��?��",
    "346": "?��?��조선",
    "082": "�??��?���?",
    "123": "조세?���?",
    "029": "?���??��????��?��",
    "607": "?��?��????��",
    "660": "kbc광주방송",
    "003": "?��?��?��",
    "374": "SBS Biz",
    "215": "?���?경제TV",
    "293": "블로?��",
    "586": "?��?��????��",
    "030": "?��?��?���?",
    "448": "TV조선",
    "138": "?���??��?��?���?",
    "092": "�??��?��코리?��",
    "262": "?��?��?��",
    "044": "코리?��?��?��?��",
    "127": "기자?��?���?",
    "662": "?��민신�?",
    "002": "?��?��?��?��",
    "050": "?��경비즈니?��",
    "666": "경기?���?",
    "654": "강원?��민일�?",
    "094": "?���? ?��",
    "656": "????��?���?",
    "024": "매경?��코노�?",
    "658": "�??��?���?",
    "308": "?��?��IN",
    "640": "코리?��중앙?��?���?",
    "243": "?��코노미스?��",
    "417": "머니S",
    "310": "?��?��?���?",
    "659": "?��주MBC",
    "036": "?��겨레21",
    "661": "JIBS",
    "033": "주간경향",
    "007": "?��?��",
    "657": "???구MBC",
    "037": "주간?��?��",
    "655": "CJB�?주방?��",
    "665": "?��?��쿠프",
    "353": "중앙SUNDAY",
    "145": "?��?��?��경향"
}


# ?��?���? API ?���? ?���?
CLIENT_ID = "bAH1YsUVJACd04LZpvmx"  # 발급받�?? ?��?��?��?��?�� ID
CLIENT_SECRET = "QRde3I7aiD"  # 발급받�?? ?��?��?��?��?�� ?��?���?


async def fetch_naver_news(session, query, display=100, start=1, sort="date"):
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


# URL?��?�� ?��론사 ID 추출 ?��?��
def find_office_id(url):
    match = re.search(r'/article/(\d+)/', url)
    if match:
        office_id = match.group(1)
        return press_dict.get(office_id, "")
    return None


# ?��?�� 링크 �??��?���?
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
# asyncio ?��?��
if __name__ == "__main__":
    asyncio.run(main())
'''
