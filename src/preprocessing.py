import pandas as pd

def process_players_to_df(players_json):
    """
    Enhanced player stats extraction including defense, attack, and discipline.
    """
    players_list = []
    for entry in players_json:
        player = entry['player']
        stats = entry['statistics'][0]
        
        players_list.append({
            'name': player['name'],
            'team': stats['team']['name'],
            'age': player['age'],
            'nationality': player['nationality'],
            'rating': float(stats['games'].get('rating', 0) or 0),
            'goals': stats['goals'].get('total', 0) or 0,
            'assists': stats['goals'].get('assists', 0) or 0,
            'shots': stats['shots'].get('total', 0) or 0,
            'passes': stats['passes'].get('total', 0) or 0,
            'key_passes': stats['passes'].get('key', 0) or 0,
            'tackles': stats['tackles'].get('total', 0) or 0,
            'interceptions': stats['tackles'].get('interceptions', 0) or 0,
            'dribbles': stats['dribbles'].get('success', 0) or 0,
            'yellow_cards': stats['cards'].get('yellow', 0) or 0,
            'red_cards': stats['cards'].get('red', 0) or 0
        })
    return pd.DataFrame(players_list)

def process_fixtures_to_df(fixtures_json):
    matches = []
    for fixture in fixtures_json:
        match = {
            'fixture_id': fixture['fixture']['id'],
            'home_team': fixture['teams']['home']['name'],
            'away_team': fixture['teams']['away']['name'],
            'home_team_id': fixture['teams']['home']['id'],
            'away_team_id': fixture['teams']['away']['id']
        }
        matches.append(match)
    return pd.DataFrame(matches)

def engineer_features(df):
    """
    Feature engineering for XGBoost.
    """
    # Mock for demo, ideally you'd merge historical team performance.
    df['Home_Form'] = 2.5 
    df['Away_Form'] = 1.2
    df['GD_L5'] = 3
    return df
