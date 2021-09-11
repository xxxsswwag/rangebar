from sqlalchemy import create_engine

from tables import Base
from configuration import settings as s


def main():
    engine = create_engine(f"{s.db}+{s.module}://{s.db_user}@{s.host}:{s.port}/{s.base}", echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()