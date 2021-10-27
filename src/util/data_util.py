import datetime
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from sklearn import linear_model


def month_growth(df):
    try:
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


def linear_regression(dict, dates_array):
    try:
        lm = linear_model.LinearRegression()

        df_dict = pd.DataFrame.from_dict(dict)

        df_date = pd.DataFrame(df_dict['date'])
        df_sum = pd.DataFrame(df_dict['sum'])

        df_date['date'] = pd.to_datetime(df_date['date'])

        df_date['date'] = df_date['date'].map(datetime.datetime.toordinal)

        model = lm.fit(df_date, df_sum)

        month_list = dates_array.copy()

        for i in range(1, 4):
            month_list.append((datetime.date.today() + relativedelta(months=+i)).strftime('%m/%Y'))

        X = pd.DataFrame(month_list, columns=['date'])
        X['date'] = pd.to_datetime(X['date'])
        X['date'] = X['date'].map(datetime.datetime.toordinal)

        Y = model.predict(X)
        Y = pd.DataFrame(Y, columns=['prediction'])

        df = pd.concat([X, Y], axis=1)

        df['date'] = df['date'].map(datetime.datetime.fromordinal)
        df['date'] = df['date'].dt.strftime('%m/%Y')

        df = df.astype({'prediction': int})

        df['prediction'] = np.where(df.prediction < 0, 0, df.prediction)

        df.loc[df.date.isin(dates_array), 'prediction'] = -1

        linear_regression_dict = df.to_dict('records')

        return linear_regression_dict

    except(Exception):
        return None


def get_sorted_array(query_array):
    dates_array = [x[0].strftime('%m/%Y') for x in query_array]
    dates_array = list(set(dates_array))

    dates_new = [datetime.datetime.strptime(x, '%m/%Y') for x in dates_array]

    dates_new.sort(reverse=True)

    dates_last_three_months = dates_new[:3]

    dates_last_three_months.sort()

    dates_last_three_months_strf = [x.strftime('%m/%Y') for x in dates_last_three_months]

    return dates_last_three_months_strf


def total_average(comments_age_average_df, likes_age_average_df):
    df_concat = pd.concat([comments_age_average_df, likes_age_average_df])

    df_sum = df_concat['timedelta'].sum()

    count = df_concat.shape[0]

    try:
        average = int(df_sum / count)

    except(Exception):
        average = 0

    return average
