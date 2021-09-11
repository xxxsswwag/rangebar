from pydantic import BaseSettings


class Settings(BaseSettings):
    db: str = 'postgresql'
    module: str = 'psycopg2'
    db_user: str = 'userbinance'
    base: str = 'candlesticks'
    host: str = 'localhost'
    port: int = 5432


settings = Settings()