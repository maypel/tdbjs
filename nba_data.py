import datetime as dt
import pandas as pd
import requests
import json
# from pandas_datareader import data as pdr


def recherche_1():

    # response = requests.get(url="https://www.nba.com/games")
    response = requests.get(url="https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json")
    content = json.loads(response.content.decode('utf-8'))
    print(f"api_news content : {content}")
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

    # Afficher le DataFrame
    df




def recherche_2():
    response = requests.get(url="https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=Rookies&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS")
    content = json.loads(response.content.decode('utf-8'))
    print(f"content : {content}")

    df = pd.DataFrame(content['resultSet']['rowSet'], columns=content['resultSet']['headers'])

    print(df)

    # Filtrer les dix premiers joueurs
    top_ten_players = df.head(10)

    # Afficher le résultat
    print(top_ten_players)

    # Filtrer les résultats de Victor Wembanyama
    wembanyama_results = df[df['PLAYER'] == 'Victor Wembanyama']

    # Afficher le résultat
    print(wembanyama_results)


if __name__ == "__main__":
    recherche_1()