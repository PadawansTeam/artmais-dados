from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base

class UsuariosModel(declarative_base()):
    __tablename__ = 'usuario'

    idusuario = Column(Integer, primary_key=True)
    datanasc = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idusuario}>"
