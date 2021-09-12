from pydantic import BaseSettings


class Settings(BaseSettings):
    db: str = 'postgresql'
    module: str = 'psycopg2'
    username: str = 'userbinance'
    base: str = 'candlesticks'
    host: str = 'localhost'
    port: int = 5432
    table = 'range_bar'


class SettingsWS(BaseSettings):
    ws: str = 'ws'
    wss: str = 'wss'
    binance: str = 'fstream.binance.com/ws'
    stream: str = 'aggTrade'


ws_settings = SettingsWS()
db_settings = Settings()