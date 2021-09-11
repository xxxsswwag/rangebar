from typing import List, Dict, Any

import ccxt
from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configuration import settings as s

Base = declarative_base()
engine = create_engine(f"{s.db}+{s.module}://{s.db_user}@{s.host}:{s.port}/{s.base}", echo=False)


class RangeBar(Base):
    __table__ = Table("range_bar", MetaData(bind=engine), autoload=True)


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
    rangebar = rangebar(split_list(arr=get_agg_trade, size=10))

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for rbar in rangebar:
        r = RangeBar(
            timestamp=rbar['T'],
            volume=rbar['v'],
            open=rbar['o'],
            high=rbar['h'],
            low=rbar['l'],
            close=rbar['c'],
        )
        session.add(r)
    session.commit()
