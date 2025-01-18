import re

import aiohttp

# 1? κ°?κΉμΈ?λ‘? μ§λ³΄, 10? κ°?κΉμΈ?λ‘? λ³΄μ

press_dict = {
    "018": "?΄?°?Όλ¦?",
    "088": "λ§€μΌ? λ¬?",
    "214": "MBC",
    "015": "?κ΅?κ²½μ ",
    "052": "YTN",
    "008": "λ¨Έλ?¬?°?΄",
    "032": "κ²½ν₯? λ¬?",
    "366": "μ‘°μ λΉμ¦",
    "005": "κ΅?λ―ΌμΌλ³?",
    "023": "μ‘°μ ?Όλ³?",
    "081": "??Έ? λ¬?",
    "025": "μ€μ?Όλ³?",
    "087": "κ°μ?Όλ³?",
    "469": "?κ΅??Όλ³?",
    "006": "λ―Έλ?΄?€?",
    "421": "?΄?€1",
    "001": "?°?©?΄?€",
    "422": "?°?©?΄?€TV",
    "437": "JTBC",
    "011": "??Έκ²½μ ",
    "057": "MBN",
    "055": "SBS",
    "031": "??΄?΄?€24",
    "021": "λ¬Έν?Όλ³?",
    "119": "?°?Όλ¦¬μ",
    "053": "μ£Όκ°μ‘°μ ",
    "296": "μ½λ©??·μ»?",
    "009": "λ§€μΌκ²½μ ",
    "028": "?κ²¨λ ",
    "016": "?€?΄?κ²½μ ",
    "014": "??΄?Έ??΄?€",
    "056": "KBS",
    "047": "?€λ§μ΄?΄?€",
    "584": "???¬?΄?Έ?€",
    "079": "?Έμ»·λ΄?€",
    "449": "μ±λA",
    "277": "???κ²½μ ",
    "022": "?Έκ³μΌλ³?",
    "020": "???Όλ³?",
    "648": "λΉμ¦?μΉ?",
    "629": "??©?Έ",
    "346": "?¬?€μ‘°μ ",
    "082": "λΆ??°?Όλ³?",
    "123": "μ‘°μΈ?Όλ³?",
    "029": "?μ§??Έ?????€",
    "607": "?΄?€????",
    "660": "kbcκ΄μ£Όλ°©μ‘",
    "003": "?΄??€",
    "374": "SBS Biz",
    "215": "?κ΅?κ²½μ TV",
    "293": "λΈλ‘?°",
    "586": "??¬????",
    "030": "? ?? λ¬?",
    "448": "TVμ‘°μ ",
    "138": "?μ§??Έ?°?Όλ¦?",
    "092": "μ§???·μ½λ¦¬?",
    "262": "? ??",
    "044": "μ½λ¦¬??€?΄?",
    "127": "κΈ°μ??λ³?",
    "662": "?λ―Όμ λ¬?",
    "002": "?? ??",
    "050": "?κ²½λΉμ¦λ?€",
    "666": "κ²½κΈ°?Όλ³?",
    "654": "κ°μ?λ―ΌμΌλ³?",
    "094": "?κ°? ?°",
    "656": "???? ?Όλ³?",
    "024": "λ§€κ²½?΄μ½λΈλ―?",
    "658": "κ΅?? ? λ¬?",
    "308": "??¬IN",
    "640": "μ½λ¦¬?μ€μ?°?Όλ¦?",
    "243": "?΄μ½λΈλ―Έμ€?Έ",
    "417": "λ¨ΈλS",
    "310": "?¬?±? λ¬?",
    "659": "? μ£ΌMBC",
    "036": "?κ²¨λ 21",
    "661": "JIBS",
    "033": "μ£Όκ°κ²½ν₯",
    "007": "?Ό?€",
    "657": "???κ΅¬MBC",
    "037": "μ£Όκ°??",
    "655": "CJBμ²?μ£Όλ°©?‘",
    "665": "??€μΏ ν",
    "353": "μ€μSUNDAY",
    "145": "? ?΄?κ²½ν₯"
}


# ?€?΄λ²? API ?Έμ¦? ? λ³?
CLIENT_ID = "bAH1YsUVJACd04LZpvmx"  # λ°κΈλ°μ?? ?΄?Ό?΄?Έ?Έ ID
CLIENT_SECRET = "QRde3I7aiD"  # λ°κΈλ°μ?? ?΄?Ό?΄?Έ?Έ ??¬λ¦?


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


# URL?? ?Έλ‘ μ¬ ID μΆμΆ ?¨?
def find_office_id(url):
    match = re.search(r'/article/(\d+)/', url)
    if match:
        office_id = match.group(1)
        return press_dict.get(office_id, "")
    return None


# ?΄?€ λ§ν¬ κ°?? Έ?€κΈ?
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
# asyncio ?€?
if __name__ == "__main__":
    asyncio.run(main())
'''
