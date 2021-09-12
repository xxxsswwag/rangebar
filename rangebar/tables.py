from sqlalchemy import Column, Integer, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base
from configuration import db_settings as db
Base = declarative_base()


class RangeBar(Base):
    __tablename__ = db.table
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(BigInteger)
    volume = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


# class RangeBar(Base):
#     __table__ = Table("range_bar", self.metadata, autoload=True)
#
#     def __init__(self, metadata):
#         self.metadata = MetaData(engine)
