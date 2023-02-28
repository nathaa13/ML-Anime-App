from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
#from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import start_http_server, Summary, Counter, Info, make_wsgi_app
import time


app = Flask(__name__)
wsgi_app = make_wsgi_app()
#metrics = PrometheusMetrics(app)

# Define some metrics
REQUEST_COUNT = Counter('request_count', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Summary('request_latency_ms', 'Request latency in milliseconds', ['method', 'endpoint', 'http_status'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données saisies par l'utilisateur
    Title = request.form['Title']
    Genre = request.form['Genre']
    Synopsis = request.form['Synopsis']
    Type = request.form['Type']
    Producer = request.form['Producer']
    Studio = request.form['Studio']

    # Utiliser le modèle pour faire une prédiction
    new_data = pd.DataFrame({
        'Title': [Title],
        'Genre': [Genre],
        'Synopsis': [Synopsis],
        'Type': [Type],
        'Producer': [Producer],
        'Studio': [Studio]
    })
    #rating = model.predict(new_data)

    # Afficher le résultat de la prédiction à l'utilisateur
    return render_template('resultat.html', rating=Title)
    #return render_template('resultat.html', rating=jsonify({'rating':  Title + "404"}))


# Add some middleware to measure the request metrics
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.path, response.status_code).observe(latency)
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
