import pandas as pd
from sqlalchemy import func
from src.infra.factories.database_connection_factory import create
from src.domain.visit import VisitasModel
from src.util.data_util import month_growth


class VisitRepository():
    def __init__(self, user_id):
        self.user_id = user_id

    def get_visits_by_user_id(self):
        session = create()

        visits = session.query(VisitasModel.datavisita, func.count(VisitasModel.idacessoperfil)) \
            .group_by(VisitasModel.datavisita). \
            filter(VisitasModel.idusuariovisitado == self.user_id).all()

        visits_dates = [x[0].strftime('%m/%Y') for x in visits]
        idacessoperfil_visits = [x[1] for x in visits]

        df_visits = pd.DataFrame(
            {'date': visits_dates,
             'idpublicacao': idacessoperfil_visits})

        session.close()

        return month_growth(df_visits)

    def total_number_of_visits(self):
        session = create()

        visits = session.query(func.count(VisitasModel.idacessoperfil)). \
            filter(VisitasModel.idusuariovisitado == self.user_id).all()

        visits_amount = visits[0][0]

        session.close()

        return visits_amount
