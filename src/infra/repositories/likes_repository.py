
import datetime
import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.entities.like import CurtidasModel
from src.domain.entities.publication import PublicacaoModel
from src.domain.entities.user import UsuariosModel
from src.util.data_util import evolucao_mes, media_idades

class LikeRepository():
    def __init__(self, user_id):
        self.session = create()
        self.user_id = user_id

    def get_likes_by_user_id(self):
        curtidas = self.session.query(CurtidasModel.datacurtida, func.count(CurtidasModel.idpublicacao)) \
        .group_by(CurtidasModel.datacurtida). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        data_curtidas = [x[0].strftime('%m/%Y') for x in curtidas]
        idpublicacoes_curtidas = [x[1] for x in curtidas]

        df_curtidas = pd.DataFrame(
            {'data': data_curtidas,
            'idpublicacao': idpublicacoes_curtidas})

        return evolucao_mes(df_curtidas)

    def get_likes_age_average_by_user_id(self):
        media_idades_curtidas = self.session.query(CurtidasModel.idusuario, UsuariosModel.datanasc). \
        filter(CurtidasModel.idpublicacao == PublicacaoModel.idpublicacao). \
        filter(CurtidasModel.idusuario == UsuariosModel.idusuario). \
        filter(PublicacaoModel.idusuario == self.user_id).all()

        data_curtidas_idades = [x[1].strftime(
        '%Y-%m-%d') for x in media_idades_curtidas]
        idpublicacoes = [x[0] for x in media_idades_curtidas]

        df_idade_curtidas = pd.DataFrame(
        {'data': data_curtidas_idades,
         'idusuario': idpublicacoes,
         'agora': datetime.datetime.today().strftime("%Y-%m-%d")})

        return media_idades(df_idade_curtidas)
 