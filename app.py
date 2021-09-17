from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from flask import Flask, render_template, request
from flask_migrate import Migrate
import logging
import datetime

POSTGRES = {
    'user': '##',
    'pw': '##',
    'db': '##',
    'host': '##',
    'port': '##',
}

SQLALCHEMY_DATABASE_URL = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()

app = Flask(__name__, template_folder='html')


class CurtidasModel(Base):
    __tablename__ = 'curtida'

    idcurtida = Column(Integer, primary_key=True)
    idpublicacao = Column(Integer)
    datacurtida = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idusuario}>"

class ComentariosModel(Base):
    __tablename__ = 'comentario'

    idcomentario = Column(Integer, primary_key=True)
    idpublicacao = Column(Integer)
    datahora = Column(Date)

    def __repr__(self):
        return f"<IdUsuario {self.idcomentario}>"


class PublicacaoModel(Base):
    __tablename__ = 'publicacao'

    idpublicacao = Column(Integer, primary_key=True)
    idusuario = Column(Integer)

    def __repr__(self):
        return f"<IdPublicacao {self.idpublicacao}>"


@app.route('/curtidas', methods=['GET'])
def graphs():
    # filtra pelo usuario em questão
    curtidas = session.query(CurtidasModel.datacurtida, func.count(CurtidasModel.idpublicacao)).group_by(
        CurtidasModel.datacurtida). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == 151).all()

    datascurtidas = [x[0].strftime('%d/%m/%Y') for x in curtidas]
    idpublicacoes = [x[1] for x in curtidas]

    return render_template("python.component.html", labels=datascurtidas, values=idpublicacoes)

@app.route('/comentarios', methods=['GET'])
def graficos():
    # filtra pelo usuario em questão
    comentarios = session.query(ComentariosModel.datahora, func.count(ComentariosModel.idpublicacao)).group_by(
        ComentariosModel.datahora). \
        filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == 151).all()

    datascomentarios = [x[0].strftime('%d/%m/%Y') for x in comentarios]
    idpublicacoes = [x[1] for x in comentarios]

    return render_template("python.component.html", labels=datascomentarios, values=idpublicacoes)