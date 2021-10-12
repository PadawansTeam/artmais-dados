import datetime
import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.entities.comment import ComentariosModel
from src.domain.entities.publication import PublicacaoModel
from src.domain.entities.user import UsuariosModel
from src.util.data_util import evolucao_mes, media_idades

class CommentRepository():
    def __init__(self, user_id):
        self.session = create()
        self.user_id = user_id
    
    def get_comments_by_user_id(self):
        comentarios = self.session.query(ComentariosModel.datahora, func.count(ComentariosModel.idpublicacao)).group_by(
        ComentariosModel.datahora). \
        filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        data_comentarios = [x[0].strftime('%m/%Y') for x in comentarios]
        idpublicacoes_comentarios = [x[1] for x in comentarios]

        df_comentarios = pd.DataFrame(
        {'data': data_comentarios,
         'idpublicacao': idpublicacoes_comentarios})
         
        return evolucao_mes(df_comentarios)

    def get_comments_age_average_by_user_id(self):
        media_idades_comentarios = self.session.query(ComentariosModel.idusuario, UsuariosModel.datanasc). \
        filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(ComentariosModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        data_comentarios_idades = [x[1].strftime(
        '%Y-%m-%d') for x in media_idades_comentarios]
        idpublicacoes_comentarios = [x[0] for x in media_idades_comentarios]

        df_idade_comentarios = pd.DataFrame(
        {'data': data_comentarios_idades,
         'idusuario': idpublicacoes_comentarios,
         'agora': datetime.datetime.today().strftime("%Y-%m-%d")})

        return media_idades(df_idade_comentarios)