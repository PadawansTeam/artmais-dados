class PublicacaoModel(Base):
    __tablename__ = 'publicacao'

    idpublicacao = Column(Integer, primary_key=True)
    idusuario = Column(Integer)

    def __repr__(self):
        return f"<IdPublicacao {self.idpublicacao}>"
