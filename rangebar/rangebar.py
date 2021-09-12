from typing import List, Dict, Any

import ccxt
from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configuration import db_settings as db

Base = declarative_base()
engine = create_engine(f"{db.db}+{db.module}://{db.username}@{db.host}:{db.port}/{db.base}", echo=False)


class RangeBar(Base):
    __table__ = Table(db.table, MetaData(bind=engine), autoload=True)


def split_list(arr: List[Dict[str, Any]], size: int) -> List[Dict[str, float]]:
    # arr: It is a list of dictionaries with a big range of information about aggTrade
    # size: It is size for each list with dictionaries and size for a range bar
    # size=2, arr=10 = [ [], [], [], [], [] ]
    lst = []
    while len(arr) > size:
        data = arr[:size]
        lst.append(data)
        arr = arr[size:]
    lst.append(arr)
    return lst


def rangebar(lst: List[Dict[str, float]]) -> List[Dict[str, float]]:
    rb = []
    for data in lst:
        q = []
        p = []
        t = []
        for d in data:
            q.append(float(d['info']['q']))
            p.append(float(d['info']['p']))
            t.append(float(d['info']['T']))
        rb.append({"v": sum(q), "o": p[0], "h": max(p), "l": min(p), "c": p[-1], "T": max(t)})
    return rb


if __name__ == '__main__':
    binance = ccxt.binance()
    get_agg_trade = binance.fetch_trades(symbol='BTCUSDT', limit=100)
    get_rangebar = rangebar(split_list(arr=get_agg_trade, size=10))

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for bar in get_rangebar:
        r = RangeBar(
            timestamp=bar['T'],
            volume=bar['v'],
            open=bar['o'],
            high=bar['h'],
            low=bar['l'],
            close=bar['c'],
        )
        session.add(r)
    session.commit()
