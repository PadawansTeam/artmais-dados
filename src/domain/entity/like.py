from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base

class CurtidasModel(declarative_base()):
    __tablename__ = 'curtida'

    idcurtida = Column(Integer, primary_key=True)
    idusuario = Column(Integer)
    idpublicacao = Column(Integer)
    datacurtida = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idusuario}>"
