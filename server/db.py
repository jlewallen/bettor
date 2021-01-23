import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


session = None


def create():
    global session
    if session is None:
        logging.info("creating database")
        engine = create_engine("sqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)

        session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

        Base.query = session.query_property()

    return session
