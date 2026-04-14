import pandas as pd
from .models import PlayerStats, Fixture

def process_players_to_df(players_json):
    """
    Enhanced player stats extraction using Pydantic for validation.
    """
    players_list = []
    for entry in players_json:
        player_data = entry['player']
        stats_data = entry['statistics'][0]
        
        # Validate data with Pydantic
        player_stats = PlayerStats(
            name=player_data['name'],
            team=stats_data['team']['name'],
            age=player_data.get('age'),
            nationality=player_data.get('nationality'),
            rating=float(stats_data['games'].get('rating', 0) or 0),
            goals=stats_data['goals'].get('total', 0) or 0,
            assists=stats_data['goals'].get('assists', 0) or 0,
            shots=stats_data['shots'].get('total', 0) or 0,
            passes=stats_data['passes'].get('total', 0) or 0,
            key_passes=stats_data['passes'].get('key', 0) or 0,
            tackles=stats_data['tackles'].get('total', 0) or 0,
            interceptions=stats_data['tackles'].get('interceptions', 0) or 0,
            dribbles=stats_data['dribbles'].get('success', 0) or 0,
            yellow_cards=stats_data['cards'].get('yellow', 0) or 0,
            red_cards=stats_data['cards'].get('red', 0) or 0
        )
        players_list.append(player_stats.model_dump())
        
    return pd.DataFrame(players_list)

def process_fixtures_to_df(fixtures_json, league_id=None, season=None):
    """
    Process fixtures and validate with Pydantic.
    """
    matches = []
    for fixture in fixtures_json:
        # Validate with Pydantic
        match_obj = Fixture(
            fixture_id=fixture['fixture']['id'],
            home_team=fixture['teams']['home']['name'],
            away_team=fixture['teams']['away']['name'],
            home_team_id=fixture['teams']['home']['id'],
            away_team_id=fixture['teams']['away']['id'],
            league_id=league_id or fixture.get('league', {}).get('id', 0),
            season=season or fixture.get('league', {}).get('season', 0)
        )
        matches.append(match_obj.model_dump())
        
    return pd.DataFrame(matches)

def engineer_features(df):
    """
    Feature engineering for XGBoost.
    """
    # Mock for demo, ideally you'd merge historical team performance from DB.
    df['Home_Form'] = 2.5 
    df['Away_Form'] = 1.2
    df['GD_L5'] = 3
    return df
