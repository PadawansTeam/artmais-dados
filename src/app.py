from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from flask import Flask, render_template, request
from flask_migrate import Migrate
import logging
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

POSTGRES = {
    'user': '##',
    'pw': '##',
    'db': '#',
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


@app.route('/dashboard', methods=['GET'])
def graficos():
    def media_idades(df):
        df['data'] = pd.to_datetime(df['data'])
        df['agora'] = pd.to_datetime(df['agora'])
        df = df.drop_duplicates(['idusuario'])
        df['diferenca'] = ((df['agora'] - df['data']) / np.timedelta64(1, 'Y'))

        return df

    def evolucao_mes(df):
        df['soma'] = df['idpublicacao'].groupby(
            df['data']).transform('count')

        df = df.drop_duplicates('data')

        df = df.drop('idpublicacao', 1)

        return df.to_dict('records')

    # get parsed id
    idusuario = request.args.get('idusuario')

    # filtra pelo usuario em questão
    comentarios = session.query(ComentariosModel.datahora, func.count(ComentariosModel.idpublicacao)).group_by(
        ComentariosModel.datahora). \
        filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == idusuario).all()

    data_comentarios = [x[0].strftime('%m/%Y') for x in comentarios]
    idpublicacoes_comentarios = [x[1] for x in comentarios]

    df_comentarios = pd.DataFrame(
        {'data': data_comentarios,
         'idpublicacao': idpublicacoes_comentarios})

    curtidas = session.query(CurtidasModel.datacurtida, func.count(CurtidasModel.idpublicacao)) \
        .group_by(CurtidasModel.datacurtida). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == idusuario).all()

    data_curtidas = [x[0].strftime('%m/%Y') for x in curtidas]
    idpublicacoes_curtidas = [x[1] for x in curtidas]

    df_curtidas = pd.DataFrame(
        {'data': data_curtidas,
         'idpublicacao': idpublicacoes_curtidas})

    dict_comentarios = evolucao_mes(df_comentarios)
    dict_curtidas = evolucao_mes(df_curtidas)

    # ----------------
    # media de idades
    # ----------------
    mediaidades_curtidas = session.query(CurtidasModel.idusuario, UsuariosModel.datanasc). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(CurtidasModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == idusuario).all()

    mediaidades_comentarios = session.query(ComentariosModel.idusuario, UsuariosModel.datanasc). \
        filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(ComentariosModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == idusuario).all()

    data_curtidas_idades = [x[1].strftime(
        '%Y-%m-%d') for x in mediaidades_curtidas]
    idpublicacoes = [x[0] for x in mediaidades_curtidas]

    data_comentarios_idades = [x[1].strftime(
        '%Y-%m-%d') for x in mediaidades_comentarios]
    idpublicacoes_comentarios = [x[0] for x in mediaidades_comentarios]

    df_novo = pd.DataFrame(
        {'data': data_curtidas_idades,
         'idusuario': idpublicacoes,
         'agora': datetime.datetime.today().strftime("%Y-%m-%d")})

    df_idade_comentarios = pd.DataFrame(
        {'data': data_comentarios_idades,
         'idusuario': idpublicacoes_comentarios,
         'agora': datetime.datetime.today().strftime("%Y-%m-%d")})

    df_novo = media_idades(df_novo)
    df_idade_comentarios = media_idades(df_idade_comentarios)

    df_concat = pd.concat([df_novo, df_idade_comentarios])
    soma = df_concat['diferenca'].sum()
    count = df_concat.shape[0]

    media = int(soma / count)

    dict_merge = {'curtidas': dict_curtidas,
                  'comentarios': dict_comentarios, 'media': media}

    return dict_merge
