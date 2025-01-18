import re

import aiohttp

# 1?— ê°?ê¹Œìš¸?ˆ˜ë¡? ì§„ë³´, 10?— ê°?ê¹Œìš¸?ˆ˜ë¡? ë³´ìˆ˜

press_dict = {
    "018": "?´?°?¼ë¦?",
    "088": "ë§¤ì¼?‹ ë¬?",
    "214": "MBC",
    "015": "?•œêµ?ê²½ì œ",
    "052": "YTN",
    "008": "ë¨¸ë‹ˆ?ˆ¬?°?´",
    "032": "ê²½í–¥?‹ ë¬?",
    "366": "ì¡°ì„ ë¹„ì¦ˆ",
    "005": "êµ?ë¯¼ì¼ë³?",
    "023": "ì¡°ì„ ?¼ë³?",
    "081": "?„œ?š¸?‹ ë¬?",
    "025": "ì¤‘ì•™?¼ë³?",
    "087": "ê°•ì›?¼ë³?",
    "469": "?•œêµ??¼ë³?",
    "006": "ë¯¸ë””?–´?˜¤?Š˜",
    "421": "?‰´?Š¤1",
    "001": "?—°?•©?‰´?Š¤",
    "422": "?—°?•©?‰´?Š¤TV",
    "437": "JTBC",
    "011": "?„œ?š¸ê²½ì œ",
    "057": "MBN",
    "055": "SBS",
    "031": "?•„?´?‰´?Š¤24",
    "021": "ë¬¸í™”?¼ë³?",
    "119": "?°?¼ë¦¬ì•ˆ",
    "053": "ì£¼ê°„ì¡°ì„ ",
    "296": "ì½”ë©”?””?‹·ì»?",
    "009": "ë§¤ì¼ê²½ì œ",
    "028": "?•œê²¨ë ˆ",
    "016": "?—¤?Ÿ´?“œê²½ì œ",
    "014": "?ŒŒ?´?‚¸?…œ?‰´?Š¤",
    "056": "KBS",
    "047": "?˜¤ë§ˆì´?‰´?Š¤",
    "584": "?™?•„?‚¬?´?–¸?Š¤",
    "079": "?…¸ì»·ë‰´?Š¤",
    "449": "ì±„ë„A",
    "277": "?•„?‹œ?•„ê²½ì œ",
    "022": "?„¸ê³„ì¼ë³?",
    "020": "?™?•„?¼ë³?",
    "648": "ë¹„ì¦ˆ?›Œì¹?",
    "629": "?”?Œ©?Š¸",
    "346": "?—¬?Š¤ì¡°ì„ ",
    "082": "ë¶??‚°?¼ë³?",
    "123": "ì¡°ì„¸?¼ë³?",
    "029": "?””ì§??„¸????„?Š¤",
    "607": "?‰´?Š¤????ŒŒ",
    "660": "kbcê´‘ì£¼ë°©ì†¡",
    "003": "?‰´?‹œ?Š¤",
    "374": "SBS Biz",
    "215": "?•œêµ?ê²½ì œTV",
    "293": "ë¸”ë¡œ?„°",
    "586": "?‹œ?‚¬????„",
    "030": "? „??‹ ë¬?",
    "448": "TVì¡°ì„ ",
    "138": "?””ì§??„¸?°?¼ë¦?",
    "092": "ì§??””?„·ì½”ë¦¬?•„",
    "262": "?‹ ?™?•„",
    "044": "ì½”ë¦¬?•„?—¤?Ÿ´?“œ",
    "127": "ê¸°ì?˜‘?šŒë³?",
    "662": "?†ë¯¼ì‹ ë¬?",
    "002": "?”„? ˆ?‹œ?•ˆ",
    "050": "?•œê²½ë¹„ì¦ˆë‹ˆ?Š¤",
    "666": "ê²½ê¸°?¼ë³?",
    "654": "ê°•ì›?„ë¯¼ì¼ë³?",
    "094": "?›”ê°? ?‚°",
    "656": "???? „?¼ë³?",
    "024": "ë§¤ê²½?´ì½”ë…¸ë¯?",
    "658": "êµ?? œ?‹ ë¬?",
    "308": "?‹œ?‚¬IN",
    "640": "ì½”ë¦¬?•„ì¤‘ì•™?°?¼ë¦?",
    "243": "?´ì½”ë…¸ë¯¸ìŠ¤?Š¸",
    "417": "ë¨¸ë‹ˆS",
    "310": "?—¬?„±?‹ ë¬?",
    "659": "? „ì£¼MBC",
    "036": "?•œê²¨ë ˆ21",
    "661": "JIBS",
    "033": "ì£¼ê°„ê²½í–¥",
    "007": "?¼?‹¤",
    "657": "???êµ¬MBC",
    "037": "ì£¼ê°„?™?•„",
    "655": "CJBì²?ì£¼ë°©?†¡",
    "665": "?”?Š¤ì¿ í”„",
    "353": "ì¤‘ì•™SUNDAY",
    "145": "? ˆ?´?””ê²½í–¥"
}


# ?„¤?´ë²? API ?¸ì¦? ? •ë³?
CLIENT_ID = "bAH1YsUVJACd04LZpvmx"  # ë°œê¸‰ë°›ì?? ?´?¼?´?–¸?Š¸ ID
CLIENT_SECRET = "QRde3I7aiD"  # ë°œê¸‰ë°›ì?? ?´?¼?´?–¸?Š¸ ?‹œ?¬ë¦?


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


# URL?—?„œ ?–¸ë¡ ì‚¬ ID ì¶”ì¶œ ?•¨?ˆ˜
def find_office_id(url):
    match = re.search(r'/article/(\d+)/', url)
    if match:
        office_id = match.group(1)
        return press_dict.get(office_id, "")
    return None


# ?‰´?Š¤ ë§í¬ ê°?? ¸?˜¤ê¸?
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
# asyncio ?‹¤?–‰
if __name__ == "__main__":
    asyncio.run(main())
'''
