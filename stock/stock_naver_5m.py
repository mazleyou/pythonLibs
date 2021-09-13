import pandas as pd
from datetime import datetime
import pymysql
from time import sleep
import random
import requests

insert_query = """insert into sise_time(DATE,CODE,TIME,PRICE,SELLING,BUYING,VOLUME,FLUCTUATION) values (%s, %s, %s, %s, %s, %s, %s, %s)"""
select_query = """select * from stock_code"""


try:
    today_date = datetime.today().strftime("%Y%m%d")
    time = today_date + '160000'

    conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
    curs = conn.cursor()

    curs.execute(select_query)
    codes = curs.fetchall()

    for code in codes:
        for page in range(1, 43):
            url = f'https://finance.naver.com/item/sise_time.nhn?code={code[1]}&thistime={time}&page={page}'
            temp = pd.read_html(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text)[0]

            # temp = pd.read_html(url)[0]
            temp = temp.loc[temp["체결시각"].isnull() == False]
            temp['체결가'] = temp['체결가'].astype(int)
            temp['매도'] = temp['매도'].astype(int)
            temp['매수'] = temp['매수'].astype(int)
            temp['전일비'] = temp['전일비'].astype(int)
            temp['거래량'] = temp['거래량'].astype(int)
            temp['변동량'] = temp['변동량'].astype(int)

            for i, row in temp.iterrows():
                curs.execute(insert_query, (today_date, code[1], row["체결시각"], row['체결가'], row['매도'], row['매수'], row['거래량'], row['변동량']))

    conn.close()
except Exception as e:
    print(e)

