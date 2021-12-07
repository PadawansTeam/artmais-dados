from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

class MidiaModel(declarative_base()):
    __tablename__ = 'midia'

    idmidia = Column(Integer, primary_key=True)
    idtipomidia = Column(Integer)

    def __repr__(self):
        return f"<IdPublicacao {self.idmidia}>"
