import os

import numpy as np
import pandas as pd

from domain.schema.topic_schema import DomainResPostTopic
from domain.service.naverNews import fetch_naver_news, find_office_id, query_naver_links

print(os.getcwd())

async def naver_main(query):
    print(f"Query: {query}")

    urls, descriptions, titles = await query_naver_links(query)
    office_ids = [find_office_id(url) for url in urls]

    for i in range(len(office_ids)):
        if office_ids[i] is None:
            urls[i] = None
            descriptions[i] = None
            titles[i] = None

    office_ids = list(filter(None, office_ids))
    urls = list(filter(None, urls))
    descriptions = list(filter(None, descriptions))
    titles = list(filter(None, titles))

    print(len(office_ids))

    return urls, descriptions, titles, office_ids

'''
사용자 성향 정도 
[f1, f2, f3] 형태로 받음
[0] : 진보
[1] : 중도
[2] : 보수

'''
async def user_polar_result(polar: list, query: str):
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
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, 'press_list.csv')
    office_df = pd.read_csv(file_path)

    # 편향도 리스트 제작
    media_orientation = pd.Series(office_df['성향'].values, index=office_df['언론사']).to_dict()
    political_orientation = []
    for office in office_ids:
        pol = media_orientation[office]
        political_orientation.append(pol)

    print(political_orientation)

    orientation = ['진보', '중도', '보수']

    # 각 카테고리별 개수
    counts = [round(ratio * len(political_orientation)) for ratio in stds]
    print(counts)
    indices = []
    for orient, count in zip(orientation, counts):
        # 해당 성향의 인덱스를 추출
        orientation_indices = [i for i, value in enumerate(political_orientation) if value == orient]
        # np.random.choice를 사용하여 중복 없이 랜덤 인덱스 추출
        max_count = min(len(orientation_indices), count)
        random_indices = np.random.choice(orientation_indices, size=max_count, replace = False)

        # 추출된 인덱스를 int로 변환하여 리스트에 추가
        indices.extend(random_indices.astype(int).tolist())

    # 해당 인덱스
    indexes = sorted(indices)

    # 인덱스 따라 요약, 제목, 링크, 언론사, 편향 -> 리스트
    s_descriptions = [descriptions[i] for i in indexes]
    s_titles = [titles[i] for i in indexes]
    s_urls = [urls[i] for i in indexes]
    s_office = [office_ids[i] for i in indexes]
    s_bias = [political_orientation[i] for i in indexes]

    # JSON 형태로 변환
    data = []

    for i in range(len(indexes)):
        data.append(
            DomainResPostTopic(
                title=s_titles[i], # 제목
                descriptions=s_descriptions[i], # 요약
                office=s_office[i], # 언론사
                url=s_urls[i], # 뉴스 링크
                bias=s_bias[i] # 정치 성향
            )
        )

    return data, len(indexes) # data와 총 개수


'''
# asyncio 실행
if __name__ == "__main__":
    polar = [0.5, 0.3, 0.2]
    query = '대통령'
    asyncio.run(user_polar(polar, query))
'''
