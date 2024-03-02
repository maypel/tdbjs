from flask import Flask, render_template, jsonify
from conf import METEO_API_KEY, NEWS_API_KEY
from functions import extract_keywords
import json
import requests
import datetime as dt
import yfinance as yf 
from pandas_datareader import data as pdr
import pandas as pd
from googlesearch import search

# set app
app= Flask(__name__)


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
    # print(f"api_meteo content : {content}")
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
    # print(f"api_news content : {content}")

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500


    keywords, articles = extract_keywords(content["articles"])
    print(type(keywords))
    print(type(articles))
    # print(f"keywords : {keywords}")
    # print(f"articles : {articles}")
    return jsonify({
        'status'   : 'ok',
        'data'     :{
            'keywords' : keywords[:100], # On retourne uniquement les 100 premiers mots
            'articles' : articles
        }
    })

@app.route("/api/finance/")
def finance_result():

    end = dt.datetime.now()
    start = dt.datetime(2024,1,1)

    yf.pdr_override()
    df = pdr.get_data_yahoo('BTC-USD', start, end)
    print(type(df))
    df_json = df.to_dict("records") 
    # df_json = df.to_json(orient='split')
    print(1, type(df_json))
    # df.head()

    # if response.status_code != 200:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
    #     }), 500

    return jsonify({
      'status': 'ok', 
      'data': df_json
    })


@app.route("/api/nba_games/")
def recherche_1():

    # response = requests.get(url="https://www.nba.com/games")
    response = requests.get(url="https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json")
    content = json.loads(response.content.decode('utf-8'))
    # print(f"api_news content : {content}")
    data = {
    'gameTimeUTC': [],
    'homeTeamName': [],
    'homeTeamScore': [],
    'awayTeamName': [],
    'awayTeamScore': [],
    'homeLeaderName': [],
    'homeLeaderPoints': [],
    'homeLeaderRebounds': [],
    'homeLeaderAssists': [],
    'awayLeaderName': [],
    'awayLeaderPoints': [],
    'awayLeaderRebounds': [],
    'awayLeaderAssists': [],
}

    games = content['scoreboard']['games']

    for game in games:
        data['gameTimeUTC'].append(game['gameTimeUTC'])
        data['homeTeamName'].append(game['homeTeam']['teamName'])
        data['homeTeamScore'].append(game['homeTeam']['score'])
        data['awayTeamName'].append(game['awayTeam']['teamName'])
        data['awayTeamScore'].append(game['awayTeam']['score'])

        home_leader = game['gameLeaders']['homeLeaders']
        away_leader = game['gameLeaders']['awayLeaders']

        data['homeLeaderName'].append(home_leader['name'])
        data['homeLeaderPoints'].append(home_leader['points'])
        data['homeLeaderRebounds'].append(home_leader['rebounds'])
        data['homeLeaderAssists'].append(home_leader['assists'])

        data['awayLeaderName'].append(away_leader['name'])
        data['awayLeaderPoints'].append(away_leader['points'])
        data['awayLeaderRebounds'].append(away_leader['rebounds'])
        data['awayLeaderAssists'].append(away_leader['assists'])

    # Créer un DataFrame pandas
    df = pd.DataFrame(data)
    print(f"df : {df}")
    df_json = df.to_json()
    print(f"df_json : {df_json}")
    # df.head()

    # if response.status_code != 200:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
    #     }), 500

    return jsonify({
      'status': 'ok', 
      'data': df_json
    })

@app.route("/api/nba_rookies/")
def recherche_2():
    response = requests.get(url="https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=Rookies&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS")
    content = json.loads(response.content.decode('utf-8'))
    # print(f"content : {content}")

    df = pd.DataFrame(content['resultSet']['rowSet'], columns=content['resultSet']['headers'])

    # print(df)

    # Filtrer les dix premiers joueurs
    top_ten_players = df.head(10)

    # Afficher le résultat
    # print(top_ten_players)

    # Filtrer les résultats de Victor Wembanyama
    wembanyama_results = df[df['PLAYER'] == 'Victor Wembanyama']

    # Afficher le résultat
    # print(wembanyama_results)
    df_json = wembanyama_results.to_json()
    # df.head()

    # if response.status_code != 200:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
    #     }), 500

    return jsonify({
      'status': 'ok', 
      'data': df_json
    })

@app.route("/api/articles/")
def get_google_results(num_results=10):
    results = []

    try:
        query = "cours bitcoin"
        # Effectue la recherche et récupère les résultats
        for j in search(query, num_results=num_results):
            results.append({'link': j})

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return jsonify({
      'status': 'ok', 
      'data': results
    })
if __name__ == "__main__":
    app.run(debug=True)