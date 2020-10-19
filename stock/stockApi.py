import requests
import pymysql
import pandas as pd
from datetime import datetime
from xml.etree import ElementTree
import logging

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('stock2.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def priceCheck(str):
    try:
        retval = 0
        if len(str) > 0:
            str = str.replace(",", "")
            retval = int(str)
        return retval
    except ValueError as e:
        logger.error(e)
        return 0

conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
curs = conn.cursor()


# 'DataFrame.loc' 이용해서 사용할 컬럼만 추출
stock_xlsx = pd.read_excel('stock.xls', dtype={'종목코드': str, '기업명': str, '자본금(원)': str})
stock_df = stock_xlsx.loc[:, ['종목코드', '기업명', '자본금(원)']]

today_date = datetime.today().strftime("%Y%m%d")

s = 0
for i, row in stock_df.iterrows():
    # 엑셀 리스트중 자본금 하한 체크
    if priceCheck(row['자본금(원)']) > 30000000000:
        url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code=' + row['종목코드']
        res = requests.get(url)
        text = res.text[res.text.find('<?xml'):]
        root_element = ElementTree.fromstring(text)
        TBL_TimeConclude = root_element.iter(tag="TBL_TimeConclude")

        insert_sql = """insert into sise_time_api(DATE,CODE,TIME,PRICE,COMPARE,SELLING,BUYING,VOLUME,FLUCTUATION) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        dt = datetime.today().strftime("%Y%m%d")

        for element in TBL_TimeConclude:
            for i in element:
                time = i.attrib['time']
                negoprice = i.attrib['negoprice']
                Dungrak = i.attrib['Dungrak']
                Debi = i.attrib['Debi']
                sellprice = i.attrib['sellprice']
                buyprice = i.attrib['buyprice']
                amount = i.attrib['amount']
                # print(dt, row['종목코드'], time, negoprice, Debi, sellprice, buyprice, amount)
                curs.execute(insert_sql, (dt, row['종목코드'], time, negoprice, Debi, sellprice, buyprice, amount, ''))

conn.close()

