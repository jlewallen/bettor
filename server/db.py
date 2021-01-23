import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


log = logging.getLogger("bettor")
Base = declarative_base()


def create(path=None, echo=False, **kwargs):
    opening = path if path else "sqlite:///:memory:"
    log.info("creating database %s" % (opening,))
    engine = create_engine(opening, echo=echo)
    Base.metadata.create_all(engine)

    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    Base.query = session.query_property()

    return session
