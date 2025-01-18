import asyncio

import os

import csv
import pandas as pd

from naverNews import fetch_naver_news, find_office_id, query_naver_links

print(os.getcwd())

async def naver_main(query):
    print(f"Query: {query}")

    urls, descriptions, titles = await query_naver_links(query)
    office_ids = [find_office_id(url) for url in urls]

    for i in range(len(office_ids)):
        if office
    
    print(office_ids[9])

    return urls, descriptions, titles, office_ids

'''
사용자 성향 정도 
[f1, f2, f3] 형태로 받음
[0] : 진보
[1] : 중도
[2] : 보수

'''
async def user_polar(polar: list, query: str):
    urls, descriptions, titles, office_ids = await naver_main(query)
    # 역비율
    left = 1/polar[0]
    cent = 1/polar[1]
    right = 1/polar[2]
    
    # 정규화
    summ = left + cent + right 
    std_left = left/summ
    std_cent = cent/summ
    std_right = right/summ
    
    stds = [std_left, std_cent, std_right]
    
    # 언론사 편향 정보
    office_df = pd.read_csv('press_list.csv')
    office_df.head()
    of_pol_col = office_df['성향']
    
    # 편향도 리스트 제작
    political_orientation = [office_df[office_df['언론사'] == media]['성향'].values[0] for media in office_ids]
    print(political_orientation)
    
    counts = [round(ratio * len(urls)) for ratio in stds]
    
    
    
    
    
    


# asyncio 실행
if __name__ == "__main__":
    polar = [0.5, 0.3, 0.2]
    query = '대통령'
    asyncio.run(user_polar(polar, query))