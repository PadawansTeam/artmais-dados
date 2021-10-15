import datetime
import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.comment import ComentariosModel
from src.domain.publication import PublicacaoModel
from src.domain.user import UsuariosModel
from src.util.data_util import month_growth, users_age_average


class CommentRepository():
    def __init__(self, user_id):
        self.user_id = user_id

    def get_comments_by_user_id(self):
        session = create()

        comments = session.query(ComentariosModel.datahora, func.count(ComentariosModel.idpublicacao)).group_by(
            ComentariosModel.datahora). \
            filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
            filter(PublicacaoModel.idusuario == self.user_id).all()

        comments_dates = [x[0].strftime('%m/%Y') for x in comments]
        idpublicacao_comments = [x[1] for x in comments]

        df_comments = pd.DataFrame(
            {'date': comments_dates,
             'idpublicacao': idpublicacao_comments})

        session.close()

        return month_growth(df_comments)

    def get_comments_age_average_by_user_id(self):
        session = create()

        average_users_age_comments = session.query(ComentariosModel.idusuario, UsuariosModel.datanasc). \
            filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
            filter(ComentariosModel.idusuario == UsuariosModel.idusuario). \
            filter(PublicacaoModel.idusuario == self.user_id).all()

        df_age_comments = [x[1].strftime('%Y-%m-%d') for x in average_users_age_comments]
        idpublicacoes_comentarios = [x[0] for x in average_users_age_comments]

        df_idade_comentarios = pd.DataFrame(
            {'date': df_age_comments,
             'idusuario': idpublicacoes_comentarios,
             'now': datetime.datetime.today().strftime("%Y-%m-%d")})

        session.close()

        return users_age_average(df_idade_comentarios)

    def total_number_of_comments(self):
        session = create()

        comments = session.query(func.count(ComentariosModel.idpublicacao)). \
            filter(ComentariosModel.idpublicacao == PublicacaoModel.idpublicacao). \
            filter(PublicacaoModel.idusuario == self.user_id).all()

        comments_amount = [x[0] for x in comments]

        session.close()

        return comments_amount
