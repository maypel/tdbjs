from flask import Flask, render_template, jsonify
from conf import METEO_API_KEY, NEWS_API_KEY
from functions import extract_keywords
import json
import requests
# from flask_restful import Api, Resource, abort, reqparse
# from flask_sqlalchemy import SQLAlchemy

# set app et api
app= Flask(__name__)
# api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)


if METEO_API_KEY is None:
    # URL de test :
    METEO_API_URL = "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
else: 
    # URL avec clé :
    METEO_API_URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.1160819&lon=-1.9423073&appid=" + METEO_API_KEY

if NEWS_API_KEY is None:
    # URL de test :
    NEWS_API_URL = "https://s3-eu-west-1.amazonaws.com/course.oc-static.com/courses/4525361/top-headlines.json" # exemple de JSON
else:
    # URL avec clé :
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + NEWS_API_KEY

@app.route("/")
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/meteo')
def meteo():
    response = requests.get(METEO_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500

    data = []

    for prev in content["list"]:
        datetime = prev['dt'] * 1000 # conversion du timestamp en millisecondes
        temperature = prev['main']['temp'] - 273.15 # Conversion de Kelvin en °c
        temperature = round(temperature, 2) # Arrondi
        data.append([datetime, temperature])

    return jsonify({
      'status': 'ok', 
      'data': data
    })

@app.route('/api/news/')
def get_news():
 
    response = requests.get(NEWS_API_URL)

    content = json.loads(response.content.decode('utf-8'))
    print(content)

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500


    keywords, articles = extract_keywords(content["articles"])

    return jsonify({
        'status'   : 'ok',
        'data'     :{
            'keywords' : keywords[:100], # On retourne uniquement les 100 premiers mots
            'articles' : articles
        }
    })


if __name__ == "__main__":
    app.run(debug=True)