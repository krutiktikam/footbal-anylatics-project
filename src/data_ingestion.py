import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

def get_headers():
    return {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

@st.cache_data
def fetch_teams_by_league(league_id, season=2024):
    url = f"{BASE_URL}/teams"
    params = {'league': league_id, 'season': season}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        return response.json().get('response', [])
    except Exception as e:
        return []

@st.cache_data
def fetch_players_by_team(team_id, season=2024):
    url = f"{BASE_URL}/players"
    params = {'team': team_id, 'season': season}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        return response.json().get('response', [])
    except Exception as e:
        return []

@st.cache_data
def fetch_upcoming_fixtures(league_id, season=2024):
    url = f"{BASE_URL}/fixtures"
    params = {'league': league_id, 'season': season, 'next': 15}
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        return response.json().get('response', [])
    except Exception as e:
        return []
