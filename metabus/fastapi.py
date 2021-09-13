import json
from typing import Optional

import uvicorn
from fastapi import FastAPI
from dataclasses import asdict
from metabus.common.config import conf
import sqlalchemy
from metabus.common.database import init_db
from metabus.common.database import db_session
from metabus.common.models import metabus_test


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:taiholab@20.41.74.191:3306/taiholab'

def show_tables():
    queries = db_session.query(metabus_test).all()
    entries = [dict(id=q.id, title=q.title, code=q.CODE) for q in queries]
    return entries

def get_contents():
    try:
        metabus_test_entries = show_tables()
        ret_json = json.dumps(metabus_test_entries[0])
    except Exception as e:
        print(e)
    return ret_json

def create_app():
    """
    앱 함수 실행cssssssss
    :return:
    """

    c = conf()
    app = FastAPI()
    app.debug = True

    conf_dict = asdict(c)
    init_db()

    # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의

    # 라우터 정의
    print(get_contents())
    return app


app = create_app()


@app.get("/sample")
def read_root():
    ret_json = get_contents()
    return ret_json

if __name__ == "__main__":
    uvicorn.run(app="metabus.fastapi:app", host="0.0.0.0", port=8000, reload=True)