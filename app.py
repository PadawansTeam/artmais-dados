from flask import Flask
from src.app.dashboard import Dashboard
from src.app.recomendation.recomendation import Recomendation

app = Flask(__name__)

@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(user_id):
    dashboard = Dashboard(user_id=user_id)

    return dashboard.get_dashboard_data()

@app.route('/recomendation/<subcategory_id>', methods=['GET'])
def recomendation(subcategory_id):
    recomendation = Recomendation()

    return {'recommendedSubcategories':recomendation.prediction_result(int(subcategory_id))}

if __name__ == "__main__":
    app.run(host='localhost', port='8080')
