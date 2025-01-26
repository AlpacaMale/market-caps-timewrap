import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from tqdm import tqdm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config import (
    url,
    ACCEPT,
    ACCETPS_LANGUAGE,
    CONNECTION,
    CONTENT_TYPE,
    COOKIE,
    ORIGIN,
    REFERER,
    USER_AGENT,
)

# directorys
DATA_PATH = "./data"
IMG_PATH = "./img"
VIDEO_PATH = "./video"


def get_top_10_companies():
    headers = {
        "Accept": ACCEPT,
        "Accept-Language": ACCETPS_LANGUAGE,
        "Connection": CONNECTION,
        "Content-Type": CONTENT_TYPE,
        "Cookie": COOKIE,
        "Origin": ORIGIN,
        "Referer": REFERER,
        "User-Agent": USER_AGENT,
    }

    # 데이터가 시작하는 1995 5월 2일부터 오늘까지의 데이터를 받아오기
    # 시작일부터 끝나는 날까지 하루씩 더해준다.
    # total_days 는 tqdm의 진행 상태를 표현하기 위해서 일부러 만들었다.
    start_date = datetime(1995, 5, 2)
    end_date = datetime.now()
    delta = timedelta(days=1)
    total_days = (end_date - start_date).days + 1
    current_date = start_date

    # 빈 데이터프레임을 만들어주고 데이터를 계속 머지해서 최종적인 데이터를 구한다.
    ranked_companies_df = pd.DataFrame()
    for _ in tqdm(range(total_days), desc="Fetching Data"):

        # 요청의 데이터부분
        data = {
            "bld": "dbms/MDC/EASY/ranking/MDCEASY01701",
            "trdDd": current_date.strftime("%Y%m%d"),
            "itmTpCd": "1",
            "mktId": "ALL",
        }

        # 나는 서버를 공격해서 고장내려는게 아니라
        # 교육 목적에서 파이썬을 공부하는 것이기 때문에
        # 요청의 딜레이를 주고 요청을 한다.
        time.sleep(0.1)
        response = requests.post(url, headers=headers, data=data, verify=False)

        # 받아온 데이터를 데이터 프레임에 넣고 유효한 데이터라면 가공한다.
        # 이후 전체 주식 데이터와 합쳐준다.
        df = pd.DataFrame(response.json()["OutBlock_1"])
        if "ISU_ABBRV" in df.columns:
            df = df.iloc[0:9]
            df = df.set_index("ISU_ABBRV")
            df = df[["ISU_CD_FULL", "ISU_CD", "MKT_ID"]]
            ranked_companies_df = pd.concat(
                [ranked_companies_df, df], join="outer", axis=0
            ).drop_duplicates()
        current_date += delta
    ranked_companies_df.to_csv(f"./{DATA_PATH}/ranked_companies.csv")
