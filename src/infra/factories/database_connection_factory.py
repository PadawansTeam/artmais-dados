import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create():
    database_url = os.getenv('DATABASE_URL')
    print(database_url)
    engine = create_engine(database_url, echo=True)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session()
