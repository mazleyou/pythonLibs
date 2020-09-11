import requests
import pymysql
import pandas as pd
from datetime import datetime
from xml.etree import ElementTree

stock_xlsx = pd.read_excel('data.xls', dtype = {'종목코드': str})
stock_df = stock_xlsx.loc[:, ['종목코드']]

conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
curs = conn.cursor()

for i, row in stock_df.iterrows():
    if ()
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
        # print('----------------')
    # print('+++++++++++++++++++++')
conn.close()

