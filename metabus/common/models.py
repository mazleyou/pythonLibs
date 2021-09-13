from sqlalchemy import Column, Integer, String, DateTime
from metabus.common.database import Base

class metabus_test(Base):

    __tablename__ = 'metabus_test'
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    CODE = Column(Integer)

