import datetime
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from sklearn import linear_model


def month_growth(df):
    try:

        df['date'] = pd.to_datetime(df['date'])

        df['idpublicacao'] = df['idpublicacao'].astype(int)

        df = df.sort_values(by=['date'], ascending=False)

        last_three_months = []

        for i in range(-3, 1):
            last_three_months.append((datetime.date.today() +
                                      relativedelta(months=i)).strftime('%m/%Y'))

        df_last_three_months = pd.DataFrame(
            {'date': last_three_months,
             'idpublicacao': 0})

        df_last_three_months['date'] = pd.to_datetime(df_last_three_months['date'])

        df_last_three_months = df_last_three_months.sort_values(by=['date'], ascending=False)

        df = pd.concat([df, df_last_three_months]).groupby(["date"], as_index=False)["idpublicacao"]\
            .sum()

        df = df.sort_values(by=['date'], ascending=False)

        df['sum'] = df['idpublicacao'].groupby(
            df['date']).transform('sum')

        df = df.drop_duplicates('date')

        df['date'] = pd.to_datetime(df['date'])

        df = df.sort_values(by=['date'], ascending=False)

        df = df.head(3)

        df = df.sort_values(by=['date'])

        df['date'] = df['date'].dt.strftime('%m/%Y')

        df = df.drop('idpublicacao', 1)

        return df.to_dict('records')

    except(Exception):
        return None


def users_age_average(df):
    try:
        df['date'] = pd.to_datetime(df['date'])
        df['now'] = pd.to_datetime(df['now'])
        df = df.drop_duplicates(['idusuario'])
        df['timedelta'] = ((df['now'] - df['date']) / np.timedelta64(1, 'Y'))

        return df

    except(Exception):
        return 0


def linear_regression(dict):
    try:
        lm = linear_model.LinearRegression()

        df_dict = pd.DataFrame.from_dict(dict)

        df_date = pd.DataFrame(df_dict['date'])
        df_sum = pd.DataFrame(df_dict['sum'])

        df_date['date'] = pd.to_datetime(df_date['date'])

        df_date['date'] = df_date['date'].map(datetime.datetime.toordinal)

        model = lm.fit(df_date, df_sum)

        month_list = []

        for i in range(-4, 1):
            month_list.append((datetime.date.today() + relativedelta(months=+i)).strftime('%m/%Y'))

        dates_array = month_list.copy()

        for i in range(1, 4):
            dates_array.append((datetime.date.today() + relativedelta(months=+i)).strftime('%m/%Y'))

        X = pd.DataFrame(dates_array[2:], columns=['date'])

        X['date'] = pd.to_datetime(X['date'])
        X['date'] = X['date'].map(datetime.datetime.toordinal)

        Y = model.predict(X)
        Y = pd.DataFrame(Y, columns=['prediction'])

        df = pd.concat([X, Y], axis=1)

        df['date'] = df['date'].map(datetime.datetime.fromordinal)
        df['date'] = df['date'].dt.strftime('%m/%Y')

        df = df.astype({'prediction': int})

        df['prediction'] = np.where(df.prediction < 0, 0, df.prediction)

        df.loc[df.date.isin(month_list), 'prediction'] = -1

        linear_regression_dict = df.to_dict('records')

        return linear_regression_dict

    except(Exception):
        return None


def total_average(comments_age_average_df, likes_age_average_df):

    df_concat = pd.concat([comments_age_average_df, likes_age_average_df])

    df_sum = df_concat['timedelta'].sum()

    count = df_concat.shape[0]

    try:
        average = int(df_sum / count)

    except(Exception):
        average = 0

    return average

def month_grow_by_type(df, type):

    df = df[df['types'] == type]

    df['idpublicacao'] = df['idpublicacao'].astype(int)

    df = df.sort_values(by=['date'], ascending=False)

    last_three_months = []

    for i in range(-3, 1):
        last_three_months.append((datetime.date.today() +
                                    relativedelta(months=i)).strftime('%m/%Y'))

    df_last_three_months = pd.DataFrame(
        {'date': last_three_months,
            'idpublicacao': 0})

    df_last_three_months['date'] = pd.to_datetime(df_last_three_months['date'])
    df_last_three_months = df_last_three_months.sort_values(by=['date'], ascending=False)

    df = pd.concat([df, df_last_three_months]).groupby(["date", "types"], as_index=False)["idpublicacao"]\
        .sum()
    
    df = df.sort_values(by=['date'], ascending=False)

    df['sum'] = df['idpublicacao'].groupby(
        df['date']).transform('sum')

    df = df.drop_duplicates('date')

    
    for month in last_three_months:

        if(df.isin([month]).any().any() == False):
            df = df.append({'types': type, 'idpublicacao': 0, 'sum': 0, 'date': month}, ignore_index=True)

    df['date'] = pd.to_datetime(df['date'])
    
    df = df.sort_values(by=['date'], ascending=False)
    df = df.head(3)
    df = df.sort_values(by=['date'])

    df['date'] = df['date'].dt.strftime('%m/%Y')

    df = df.drop('idpublicacao', 1)
    
    return df.to_dict('records')