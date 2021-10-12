from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base

class ComentariosModel(declarative_base()):
    __tablename__ = 'comentario'

    idcomentario = Column(Integer, primary_key=True)
    idusuario = Column(Integer)
    idpublicacao = Column(Integer)
    datahora = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idcomentario}>"
