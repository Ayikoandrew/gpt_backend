from sqlmodel import SQLModel, create_engine, Session

from config import Config

settings = Config()

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_db():

    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
