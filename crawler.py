import requests
import time
import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config import (
    URL,
    ACCEPT,
    ACCETPS_LANGUAGE,
    CONNECTION,
    CONTENT_TYPE,
    COOKIE,
    ORIGIN,
    REFERER,
    REFERER_ISIF_PREFIX,
    USER_AGENT,
    DATA_PATH,
)

os.makedirs(DATA_PATH, exist_ok=True)


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
    start_date = datetime(2024, 5, 2)
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
        response = requests.post(URL, headers=headers, data=data, verify=False)

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


def get_list_dd():
    # 한국 역사상 상위 10위 안에 랭크된 기업의 정보로 상장일을 받아오는 코드
    ranked_companies_df = pd.read_csv(f"./{DATA_PATH}/ranked_companies.csv")
    ranked_companies_df = ranked_companies_df.set_index("ISU_ABBRV")

    # 헤더 설정
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

    # 표준코드, 마켓 이름을 토대로 상장일을 받아온다.
    for ISU_ABBRV in tqdm(ranked_companies_df.index, desc="Fetching Data"):
        data = {
            "isuCd": ranked_companies_df.loc[ISU_ABBRV]["ISU_CD_FULL"],
            "isuSrtCd": ranked_companies_df.loc[ISU_ABBRV]["ISU_CD"],
            "isuTp": ranked_companies_df.loc[ISU_ABBRV]["MKT_ID"],
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02103",
        }

        # 요청의 주기를 조절
        time.sleep(0.1)
        response = requests.post(URL, headers=headers, data=data, verify=False)
        data = response.json().get("LIST_DD", None) or datetime(1995, 5, 2).strftime(
            "%Y/%m/%d"
        )
        ranked_companies_df.at[ISU_ABBRV, "LIST_DD"] = data
    ranked_companies_df.to_csv(f"./{DATA_PATH}/companies_list_dd.csv")


def get_market_capitalization_history():
    # 기업들의 시가총액 히스토리를 받아오는 코드
    ranked_companies_df = pd.read_csv(f"./{DATA_PATH}/companies_list_dd.csv")

    # 상장일 혹은 1995년 5월 2일부터 정보를 받아온다.
    end_date = datetime.strptime(
        ranked_companies_df.loc[ISU_ABBRV]["LIST_DD"], "%Y/%m/%d"
    )
    today = datetime.now()
    market_caps_df = pd.DataFrame()

    # tqdm을 이용해 진척도를 표시한다.
    for ISU_ABBRV in tqdm(ranked_companies_df.index, desc="Fetching Data"):
        current_date = today
        market_cap_df = pd.DataFrame()
        while end_date <= current_date:
            if (current_date - relativedelta(years=1)) < end_date:
                strtDd = end_date.strftime("%Y%m%d")
            else:
                strtDd = (
                    current_date - relativedelta(years=1) + timedelta(days=1)
                ).strftime("%Y%m%d")
            headers = {
                "Accept": ACCEPT,
                "Accept-Language": ACCETPS_LANGUAGE,
                "Connection": CONNECTION,
                "Content-Type": CONTENT_TYPE,
                "Cookie": COOKIE,
                "Origin": ORIGIN,
                "Referer": f"{REFERER_ISIF_PREFIX}?tabIndex=0&isuCd={ranked_companies_df.loc[ISU_ABBRV]["ISU_CD_FULL"]}&isuSrtCd={ranked_companies_df.loc[ISU_ABBRV]["ISU_CD"]}&isuTp={ranked_companies_df.loc[ISU_ABBRV]["MKT_ID"]}&isuTpDtl=undefined&prodId=undefined",
                "User-Agent": USER_AGENT,
            }
            data = {
                "isuCd": ranked_companies_df.loc[ISU_ABBRV]["ISU_CD_FULL"],
                "isuSrtCd": ranked_companies_df.loc[ISU_ABBRV]["ISU_CD"],
                "isuTp": ranked_companies_df.loc[ISU_ABBRV]["MKT_ID"],
                "isuTpDtl": "undefined",
                "strtDd": strtDd,
                "endDd": current_date.strftime("%Y%m%d"),
                "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
            }

            # 요청의 주기를 조절한다.
            time.sleep(0.1)
            response = requests.post(URL, headers=headers, data=data, verify=False)
            if response.json()["output"] and response.status_code == 200:
                df = pd.DataFrame(response.json()["output"])
                df = df[["TRD_DD", "MKTCAP"]]
                df["TRD_DD"] = pd.to_datetime(df["TRD_DD"])
                df.set_index("TRD_DD", inplace=True)

                # 문자열을 숫자로 바꾸어야 한다.
                # int로 담기에 너무 큰 수여서 float으로 바꿔준다.
                df["MKTCAP"] = df["MKTCAP"].str.replace(",", "").astype(float)
                df = df.rename(columns={"MKTCAP": ISU_ABBRV})
                market_cap_df = pd.concat([market_cap_df, df])

            # timedate 모듈로는 1년단위로 뺄 수 없기때문에 relativedelta로 빼준다.
            current_date -= relativedelta(years=1)
        market_caps_df = pd.merge(
            market_caps_df,
            market_cap_df,
            how="outer",
            left_index=True,
            right_index=True,
        )

    # 데이터를 받아오는것이 끝나면 전치해준다.
    # 그럼 index를 주식으로, column을 날짜로 하는 과거 시가총액 데이터를 얻을 수 있다.
    market_caps_df = market_caps_df.T
    market_caps_df.fillna(0, inplace=True)
    market_caps_df = market_caps_df.set_index("Unnamed: 0")
    market_caps_df.to_csv(f"./{DATA_PATH}/mktcp_data.csv")
