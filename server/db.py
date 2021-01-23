import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


session = None


def create(path=None, echo=False, **kwargs):
    global session
    if session is None:
        opening = path if path else "sqlite:///:memory:"
        logging.info("creating database %s" % (opening,))
        engine = create_engine(opening, echo=echo)
        Base.metadata.create_all(engine)

        session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

        Base.query = session.query_property()

    return session


def get():
    return session
