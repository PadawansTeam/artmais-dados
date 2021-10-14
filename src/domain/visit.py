from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base

class VisitasModel(declarative_base()):
    __tablename__ = 'acessoperfil'

    idacessoperfil = Column(Integer, primary_key=True)
    idusuariovisitante = Column(Integer)
    idusuariovisitado = Column(Integer)
    datavisita = Column(Date)

    def __repr__(self):
        return f"<IdAcessoPerfil {self.idacessoperfil}>"
