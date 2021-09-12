from sqlalchemy import create_engine

from tables import Base
from configuration import db_settings as db


def main():
    engine = create_engine(f"{db.db}+{db.module}://{db.username}@{db.host}:{db.port}/{db.base}", echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()