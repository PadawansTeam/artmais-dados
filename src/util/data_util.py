import pandas as pd
import numpy as np

def evolucao_mes(df):
    df['soma'] = df['idpublicacao'].groupby(
        df['data']).transform('count')

    df = df.drop_duplicates('data')

    df = df.drop('idpublicacao', 1)

    return df.to_dict('records')

def media_idades(df):
    df['data'] = pd.to_datetime(df['data'])
    df['agora'] = pd.to_datetime(df['agora'])
    df = df.drop_duplicates(['idusuario'])
    df['diferenca'] = ((df['agora'] - df['data']) / np.timedelta64(1, 'Y'))

    return df