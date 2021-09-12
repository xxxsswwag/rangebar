import asyncio
from websockets import connect
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from configuration import db_settings as db
from configuration import ws_settings as ws


from tables import RangeBar


class BinanceWS:
    def __init__(self, symbol: str = None):
        self.symbol = symbol

    async def __aenter__(self):
        self._conn = connect(f"{ws.wss}://{ws.binance}/{self.symbol}@{ws.stream}")
        self.ws = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def receive(self):
        return await self.ws.recv()


engine = create_engine(f"{db.db}+{db.module}://{db.username}@{db.host}:{db.port}/{db.base}", echo=False)
session = Session(engine)


# noinspection PyTypeChecker
async def range_bar(symbol: str, size: int) -> BinanceWS:
    # ws_prefix = "{}@aggTrade".format(symbol.lower())
    async with BinanceWS(symbol=symbol) as aggregate:
        p, v, t = [], [], []
        while True:
            agg = json.loads(await aggregate.receive())
            p.append(float(agg['p']))
            v.append(float(agg['q']))
            t.append(float(agg['T']))
            if len(p) == size:
                rangebar = RangeBar(
                    timestamp=max(t),
                    volume=sum(v),
                    open=p[0],
                    high=max(p),
                    low=min(p),
                    close=p[-1], )

                session.add(rangebar)
                session.commit()
                p.clear()
                v.clear()
                t.clear()


if __name__ == '__main__':
    asyncio.run(range_bar(symbol='btcusdt', size=10))
