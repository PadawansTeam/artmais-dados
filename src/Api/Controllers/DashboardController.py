from flask import Flask, render_template, request
from flask_migrate import Migrate

@app.route('/dashboard', methods=['GET'])
def graficos():
    def media_idades(df):
        df['data'] = pd.to_datetime(df['data'])
        df['agora'] = pd.to_datetime(df['agora'])
        df = df.drop_duplicates(['idusuario'])
        df['diferenca'] = ((df['agora'] - df['data']) / np.timedelta64(1, 'Y'))

        return df