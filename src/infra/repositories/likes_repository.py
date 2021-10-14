import datetime
import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.like import CurtidasModel
from src.domain.publication import PublicacaoModel
from src.domain.user import UsuariosModel
from src.util.data_util import month_growth, users_age_average

class LikeRepository():
    def __init__(self, user_id):
        self.session = create()
        self.user_id = user_id

    def get_likes_by_user_id(self):
        likes = self.session.query(CurtidasModel.datacurtida, func.count(CurtidasModel.idpublicacao)) \
        .group_by(CurtidasModel.datacurtida). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        likes_dates = [x[0].strftime('%m/%Y') for x in likes]
        idpublicacao_likes = [x[1] for x in likes]

        df_likes = pd.DataFrame(
            {'date': likes_dates,
            'idpublicacao': idpublicacao_likes})

        return month_growth(df_likes)

    def get_likes_age_average_by_user_id(self):
        average_users_age_likes = self.session.query(CurtidasModel.idusuario, UsuariosModel.datanasc). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(CurtidasModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        date_likes = [x[1].strftime(
        '%Y-%m-%d') for x in average_users_age_likes]
        idpublicacao = [x[0] for x in average_users_age_likes]

        df_age_likes = pd.DataFrame(
        {'date': date_likes,
         'idusuario': idpublicacao,
         'now': datetime.datetime.today().strftime("%Y-%m-%d")})

        return users_age_average(df_age_likes)

    def total_number_of_likes(self):
        likes = self.session.query(func.count(CurtidasModel.idpublicacao)). \
            filter(CurtidasModel.idusuario == UsuariosModel.idusuario). \
            filter(PublicacaoModel.idusuario == self.user_id)

        likes_amount = [x[0] for x in likes]

        return likes_amount