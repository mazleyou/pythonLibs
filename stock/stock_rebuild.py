import pandas as pd
from datetime import datetime
import pymysql
from time import sleep
import random

conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
curs = conn.cursor(pymysql.cursors.DictCursor)

curs.execute("""select * from sise_time_update_history where state = %s""", ('END'))
rows = curs.fetchall()
for row in rows:
    curs.execute("""select * from sise_time where date = %s and code = %s""", (row['DATE'], row['CODE']))
    sise_rows = curs.fetchall()
    if len(sise_rows) > 0:
        for sise_row in sise_rows:
            print(row['PRICE'], row['SELLING'])
    else:
        curs.execute("""update sise_time_update_history set state=%s where date=%s and code=%s""", ('NONE', row['DATE'], row['CODE']))
    print(row['DATE'], row['CODE'])
    # history done update

conn.close()