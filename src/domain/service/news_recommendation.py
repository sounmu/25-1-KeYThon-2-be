import os

import numpy as np
import pandas as pd

from domain.schema.topic_schema import DomainResPostTopic
from domain.service.naverNews import find_office_id, query_naver_links

print(os.getcwd())

async def naver_main(query):
    # print(f"Query: {query}")

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
    
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, 'press_list.csv')
    office_df = pd.read_csv(file_path)

        # 예: CSV에서 'press' 열과 'bias' 열이 있다고 가정
    press_bias_map = pd.Series(
        office_df['언론사'].values, 
        index=office_df['성향']
    ).to_dict()

    # 3) 기사별 성향 파악
    political_orientation = []
    for office_id in office_ids:
        bias = press_bias_map.get(office_id, None)
        political_orientation.append(bias)

    # 4) 성향별 인덱스 묶기
    orient_dict = {
        '진보': [],
        '중도': [],
        '보수': []
    }
    for i, bias in enumerate(political_orientation):
        if bias in orient_dict:  # '진보'/'중도'/'보수' 중 하나면
            orient_dict[bias].append(i)

    # 5) 각 성향별로 최대 10개씩만 사용 (앞에서부터 10개 or 무작위)
    selected_indexes = []
    for bias_type in ['진보', '중도', '보수']:
        idx_list = orient_dict[bias_type]
        limit = min(len(idx_list), 10)
        selected_indexes.extend(idx_list[:limit])
        # 무작위 선택을 원하면 random 모듈 사용
        # random_indexes = random.sample(idx_list, limit)
        # selected_indexes.extend(random_indexes)

    selected_indexes.sort()

    # 6) 필터링된 기사만 남기기
    filtered_urls = [urls[i] for i in selected_indexes]
    filtered_desc = [descriptions[i] for i in selected_indexes]
    filtered_titl = [titles[i] for i in selected_indexes]
    filtered_offi = [office_ids[i] for i in selected_indexes]

    # print(len(office_ids))

    return filtered_urls, filtered_desc, filtered_titl, filtered_offi

'''
�궗�슜�옄 �꽦�뼢 �젙�룄
[f1, f2, f3] �삎�깭濡� 諛쏆쓬
[0] : 吏꾨낫
[1] : 以묐룄
[2] : 蹂댁닔

'''
async def user_polar_result(polar: list, query: str):
    urls, descriptions, titles, office_ids = await naver_main(query)
    # �뿭鍮꾩쑉
    left = 1/polar[0]
    cent = 1/polar[1]
    right = 1/polar[2]

    # �젙洹쒗솕
    summ = left + cent + right
    std_left = left/summ
    std_cent = cent/summ
    std_right = right/summ

    stds = [std_left, std_cent, std_right]

    # �뼵濡좎궗 �렪�뼢 �젙蹂�
    curr_dir = os.path.dirname(__file__)
    file_path = os.path.join(curr_dir, 'press_list.csv')
    office_df = pd.read_csv(file_path)

    # �렪�뼢�룄 由ъ뒪�듃 �젣�옉
    media_orientation = pd.Series(office_df['�꽦�뼢'].values, index=office_df['�뼵濡좎궗']).to_dict()
    political_orientation = []
    for office in office_ids:
        pol = media_orientation[office]
        political_orientation.append(pol)

    # print(political_orientation)

    orientation = ['吏꾨낫', '以묐룄', '蹂댁닔']

    # 媛� 移댄뀒怨좊━蹂� 媛쒖닔
    counts = [round(ratio * len(political_orientation)) for ratio in stds]
    # print(counts)
    indices = []
    for orient, count in zip(orientation, counts):
        # �빐�떦 �꽦�뼢�쓽 �씤�뜳�뒪瑜� 異붿텧
        orientation_indices = [i for i, value in enumerate(political_orientation) if value == orient]
        # np.random.choice瑜� �궗�슜�븯�뿬 以묐났 �뾾�씠 �옖�뜡 �씤�뜳�뒪 異붿텧
        max_count = min(len(orientation_indices), count)
        random_indices = np.random.choice(orientation_indices, size=max_count, replace = False)

        # 異붿텧�맂 �씤�뜳�뒪瑜� int濡� 蹂��솚�븯�뿬 由ъ뒪�듃�뿉 異붽��
        indices.extend(random_indices.astype(int).tolist())

    # �빐�떦 �씤�뜳�뒪
    indexes = sorted(indices)

    # �씤�뜳�뒪 �뵲�씪 �슂�빟, �젣紐�, 留곹겕, �뼵濡좎궗, �렪�뼢 -> 由ъ뒪�듃
    s_descriptions = [descriptions[i] for i in indexes]
    s_titles = [titles[i] for i in indexes]
    s_urls = [urls[i] for i in indexes]
    s_office = [office_ids[i] for i in indexes]
    s_bias = [political_orientation[i] for i in indexes]

    # JSON �삎�깭濡� 蹂��솚
    data = []

    for i in range(len(indexes)):
        data.append(
            DomainResPostTopic(
                title=s_titles[i], # �젣紐�
                descriptions=s_descriptions[i], # �슂�빟
                office=s_office[i], # �뼵濡좎궗
                url=s_urls[i], # �돱�뒪 留곹겕
                bias=s_bias[i] # �젙移� �꽦�뼢
            )
        )

    return data, len(indexes) # data��� 珥� 媛쒖닔


'''
# asyncio �떎�뻾
if __name__ == "__main__":
    polar = [0.5, 0.3, 0.2]
    query = '����넻�졊'
    asyncio.run(user_polar(polar, query))
'''
