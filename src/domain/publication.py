from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

class PublicacaoModel(declarative_base()):
    __tablename__ = 'publicacao'

    idpublicacao = Column(Integer, primary_key=True)
    idusuario = Column(Integer)
    idmidia = Column(Integer)

    def __repr__(self):
        return f"<IdPublicacao {self.idpublicacao}>"
