from flask import Flask, render_template, jsonify
from conf import METEO_API_KEY
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
    METEO_API_URL = "https://api.openweathermap.org/data/2.5/forecast?lat=48.883587&lon=2.333779&appid=" + METEO_API_KEY


@app.route("/")
def hello():
    return "Hello baby"

@app.route("/dashboard/")
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/meteo/')
def meteo():
    dictionnaire = {
        'type': 'Prévision de température',
        'valeurs': [24, 24, 25, 26, 27, 28],
        'unite': "degrés Celcius"
    }
    return jsonify(dictionnaire)




if __name__=="__main__":
    app.run(debug=True)