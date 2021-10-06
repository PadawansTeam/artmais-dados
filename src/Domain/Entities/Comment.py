class ComentariosModel(Base):
    __tablename__ = 'comentario'

    idcomentario = Column(Integer, primary_key=True)
    idusuario = Column(Integer)
    idpublicacao = Column(Integer)
    datahora = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idcomentario}>"
