import datetime
import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.like import CurtidasModel
from src.domain.publication import PublicacaoModel
from src.domain.user import UsuariosModel
from src.domain.media import MidiaModel
from src.util.data_util import month_growth, users_age_average, month_grow_by_type
from dateutil.relativedelta import relativedelta


class LikeRepository():
    def __init__(self, user_id):
        self.user_id = user_id

    def get_likes_by_user_id(self):
        session = create()

        likes = session.query(CurtidasModel.datacurtida, func.count(CurtidasModel.idpublicacao)) \
        .group_by(CurtidasModel.datacurtida). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        session.close()

        likes_dates = [x[0].strftime('%m/%Y') for x in likes]
        idpublicacao_likes = [x[1] for x in likes]

        df_likes = pd.DataFrame(
            {'date': likes_dates,
             'idpublicacao': idpublicacao_likes})

        return month_growth(df_likes)

    def get_likes_age_average_by_user_id(self):
        session = create()

        average_users_age_likes = session.query(CurtidasModel.idusuario, UsuariosModel.datanasc). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(CurtidasModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        date_likes = [x[1].strftime('%Y-%m-%d') for x in average_users_age_likes]
        idpublicacao = [x[0] for x in average_users_age_likes]

        df_age_likes = pd.DataFrame(
            {'date': date_likes,
             'idusuario': idpublicacao,
             'now': datetime.datetime.today().strftime("%Y-%m-%d")})

        session.close()

        return users_age_average(df_age_likes)

    def total_number_of_likes(self):
        session = create()

        likes = session.query(func.count(CurtidasModel.idpublicacao)). \
            filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
            filter(PublicacaoModel.idusuario == self.user_id).all()

        likes_amount = likes[0][0]

        session.close()

        return likes_amount

    def total_number_of_likes_by_media_type(self):
        session = create()

        likes_by_media_type = session.query(MidiaModel.idtipomidia, CurtidasModel.datacurtida, 
            func.count(CurtidasModel.idpublicacao)).group_by(MidiaModel.idtipomidia, CurtidasModel.datacurtida). \
            filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
            filter(PublicacaoModel.idmidia == MidiaModel.idmidia). \
            filter(PublicacaoModel.idusuario == self.user_id).all()

        types = [x[0] for x in likes_by_media_type]
        likes_dates = [x[1].strftime('%m/%Y') for x in likes_by_media_type]
        idpublicacao = [x[2] for x in likes_by_media_type]


        transdict = {1: 'Imagem',
             2: 'Video',
             3: 'Audio',
             4: 'Midia Externa',
        }

        types = [transdict[number] for number in types]

        df_likes_by_media_type = pd.DataFrame(
            {'types': types,
             'idpublicacao': idpublicacao,
             'date': likes_dates})


        session.close()


        return df_likes_by_media_type
