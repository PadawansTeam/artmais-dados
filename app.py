from flask import Flask
from src.application.dashboard import Dashboard

app = Flask(__name__)

@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(user_id):
    dashboard = Dashboard(user_id=user_id)

    return dashboard.get_dashboard_data()

if __name__ == "__main__":
    app.run(host='localhost', port='8080')