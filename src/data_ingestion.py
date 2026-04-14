import os
import requests
import streamlit as st
from dotenv import load_dotenv
from .database import SessionLocal, TeamDB, PlayerDB, FixtureDB, is_cache_valid
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

def get_headers():
    return {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

def fetch_teams_by_league(league_id, season=2024):
    db = SessionLocal()
    cached_teams = db.query(TeamDB).filter(TeamDB.league_id == league_id, TeamDB.season == season).all()
    
    # Check if cache is valid (e.g., 24 hours)
    if cached_teams and all(is_cache_valid(t.last_updated) for t in cached_teams):
        db.close()
        return [{"team": {"id": t.id, "name": t.name, "logo": t.logo}} for t in cached_teams]

    # If not in cache or expired, fetch from API
    url = f"{BASE_URL}/teams"
    params = {'league': league_id, 'season': season}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        data = response.json().get('response', [])
        
        # Update cache
        if data:
            # Delete old entries if any
            db.query(TeamDB).filter(TeamDB.league_id == league_id, TeamDB.season == season).delete()
            for entry in data:
                team = entry['team']
                db_team = TeamDB(id=team['id'], name=team['name'], league_id=league_id, season=season, logo=team.get('logo'), last_updated=datetime.utcnow())
                db.add(db_team)
            db.commit()
        
        db.close()
        return data
    except Exception as e:
        db.close()
        return []

def fetch_players_by_team(team_id, season=2024):
    db = SessionLocal()
    cached_players = db.query(PlayerDB).filter(PlayerDB.team_id == team_id, PlayerDB.season == season).first()
    
    if cached_players and is_cache_valid(cached_players.last_updated):
        db.close()
        return cached_players.data

    url = f"{BASE_URL}/players"
    params = {'team': team_id, 'season': season}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        data = response.json().get('response', [])
        
        if data:
            # Update cache
            db.query(PlayerDB).filter(PlayerDB.team_id == team_id, PlayerDB.season == season).delete()
            db_player = PlayerDB(team_id=team_id, season=season, data=data, last_updated=datetime.utcnow())
            db.add(db_player)
            db.commit()
            
        db.close()
        return data
    except Exception as e:
        db.close()
        return []

def fetch_upcoming_fixtures(league_id, season=2024):
    db = SessionLocal()
    cached_fixtures = db.query(FixtureDB).filter(FixtureDB.league_id == league_id, FixtureDB.season == season).first()
    
    # For fixtures, maybe cache for shorter time (e.g., 1 hour)
    if cached_fixtures and is_cache_valid(cached_fixtures.last_updated, hours=1):
        db.close()
        return cached_fixtures.data

    url = f"{BASE_URL}/fixtures"
    params = {'league': league_id, 'season': season, 'next': 15}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        data = response.json().get('response', [])
        
        if data:
            # Update cache
            db.query(FixtureDB).filter(FixtureDB.league_id == league_id, FixtureDB.season == season).delete()
            db_fixture = FixtureDB(league_id=league_id, season=season, data=data, last_updated=datetime.utcnow())
            db.add(db_fixture)
            db.commit()
            
        db.close()
        return data
    except Exception as e:
        db.close()
        return []
