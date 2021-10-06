class UsuariosModel(Base):
    __tablename__ = 'usuario'

    idusuario = Column(Integer, primary_key=True)
    datanasc = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idusuario}>"
