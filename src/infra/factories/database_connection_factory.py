import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

def create():
    database_url = os.getenv('DATABASE')
    
    engine = create_engine(database_url, echo=True, poolclass=NullPool)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session()
