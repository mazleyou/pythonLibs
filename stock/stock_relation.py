import pandas as pd
from datetime import datetime
import pymysql
from time import sleep
import random

conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
curs = conn.cursor(pymysql.cursors.DictCursor)

curs.execute("""select max(date) as maxdate from sise_up""")
maxdate = curs.fetchone()


curs.execute("""select * from sise_up where date = %s""", maxdate['maxdate'])
rows = curs.fetchall()
conn.close()

for index_time in range(1, 12):
    now_codes = list(row['CODE'] for row in rows if row['TIME'] == index_time)
    next_codes = list(row['CODE'] for row in rows if row['TIME'] == index_time + 1)
    for nowcode in now_codes:
        for nextcode in next_codes:
            codes = nowcode + nextcode
            conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                                   charset='utf8', autocommit=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute("""select count from sise_count where codes = %s""", codes)
            count = curs.fetchone()
            if count is None:
                curs.execute("""insert into sise_count(CODES) values (%s)""", codes)
            else:
                curs.execute("""update sise_count set count=%s where codes=%s""", (str(count['count'] + 1), codes))
            conn.close()