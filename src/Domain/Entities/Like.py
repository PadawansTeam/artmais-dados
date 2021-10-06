class CurtidasModel(Base):
    __tablename__ = 'curtida'

    idcurtida = Column(Integer, primary_key=True)
    idusuario = Column(Integer)
    idpublicacao = Column(Integer)
    datacurtida = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idusuario}>"
