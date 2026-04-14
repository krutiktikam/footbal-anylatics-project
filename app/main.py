import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Add src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import fetch_upcoming_fixtures, fetch_players_by_team, fetch_teams_by_league
from src.preprocessing import process_fixtures_to_df, engineer_features, process_players_to_df
from src.predictor import Predictor
from src.scraper import FBRefScraper

# --- Page Config & "Sporty" Aesthetic CSS ---
st.set_page_config(page_title="Football Any-latics Pro", layout="wide", page_icon="⚽")

# Custom Sporty CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1c24;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 20px;
        color: #00ff00 !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ff00 !important;
        color: #0e1117 !important;
    }
    .metric-card {
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #00ff00;
        text-align: center;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #00ff00 !important;
        font-family: 'Arial Black', Gadget, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚽ Football Any-latics Pro")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Live Match Predictions", "⚔️ Advanced Player Comparison"])

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/football.png")
st.sidebar.header("Control Center")
leagues = {'Premier League': 39, 'La Liga': 140, 'Bundesliga': 78, 'Serie A': 135, 'Ligue 1': 61}
league_name = st.sidebar.selectbox('League', list(leagues.keys()))
league_id = leagues[league_name]
season = st.sidebar.number_input("Season", 2020, 2026, 2024)

# Cache teams
if 'teams_list' not in st.session_state or st.sidebar.button("Refresh League Data", key='refresh_league_btn'):
    with st.spinner("Loading teams..."):
        teams_resp = fetch_teams_by_league(league_id, season)
        if teams_resp:
            st.session_state['teams_list'] = {t['team']['name']: t['team']['id'] for t in teams_resp}

# --- Tab 1: Live Predictions ---
with tab1:
    st.header(f"Next 15 Fixtures: {league_name}")
    if st.button("Generate AI Predictions", key='predict_btn'):
        with st.spinner("Crunching data..."):
            fixtures = fetch_upcoming_fixtures(league_id, season)
            if fixtures:
                df = process_fixtures_to_df(fixtures, league_id, season)
                df = engineer_features(df)
                predictor = Predictor()
                results = predictor.predict(df)
                
                # Visual enhancements for results table
                st.table(results[['home_team', 'away_team', 'HomeWinProbability', 'AwayWinProbability']].style.format({
                    'HomeWinProbability': "{:.2%}",
                    'AwayWinProbability': "{:.2%}"
                }))
            else:
                st.error("No upcoming fixtures found.")

# --- Tab 2: Advanced Player Comparison ---
with tab2:
    st.header("Player vs Player Performance Matrix")
    
    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        if st.button("🚀 Scrape High-Quality Stats (FBRef)", key='scrape_fbref_btn'):
            with st.spinner(f"Scraping {league_name} from FBRef... this might take a few seconds."):
                scraper = FBRefScraper()
                scraped_data = scraper.scrape_players_by_league(league_name)
                if scraped_data:
                    st.session_state['scraped_df'] = pd.DataFrame(scraped_data)
                    st.success(f"Loaded {len(scraped_data)} players with advanced stats!")
                else:
                    st.error("Could not scrape data. FBRef might be blocking or the URL changed.")

    if 'teams_list' in st.session_state:
        teams = st.session_state['teams_list']
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.subheader("Selection A")
            t1_name = st.selectbox("Club A", list(teams.keys()), key='t1_select_box')
            if st.button(f"Load {t1_name} Roster (API)", key='t1_load_btn'):
                p_resp = fetch_players_by_team(teams[t1_name], season)
                st.session_state['p1_df'] = process_players_to_df(p_resp)
        
        with col_t2:
            st.subheader("Selection B")
            t2_name = st.selectbox("Club B", list(teams.keys()), key='t2_select_box')
            if st.button(f"Load {t2_name} Roster (API)", key='t2_load_btn'):
                p_resp = fetch_players_by_team(teams[t2_name], season)
                st.session_state['p2_df'] = process_players_to_df(p_resp)

        # Merge data from both sources if available
        all_players = pd.DataFrame()
        if 'scraped_df' in st.session_state:
            all_players = st.session_state['scraped_df']
        elif 'p1_df' in st.session_state and 'p2_df' in st.session_state:
            p1_df = st.session_state['p1_df']
            p2_df = st.session_state['p2_df']
            if not p1_df.empty or not p2_df.empty:
                all_players = pd.concat([p1_df, p2_df]).drop_duplicates(subset=['name'])
        
        if not all_players.empty:
            selected = st.multiselect("Compare Players (Up to 4)", all_players['name'].tolist(), key='player_compare_select')
            
            if selected:
                comp_df = all_players[all_players['name'].isin(selected)]
                
                # Metric Cards
                m_cols = st.columns(len(selected))
                for idx, row in enumerate(comp_df.itertuples()):
                    with m_cols[idx]:
                        rating_val = getattr(row, 'rating', 0)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{row.name}</h3>
                            <p style="font-size: 18px; color: #00ff00;">{row.team}</p>
                            <p>Goals: {row.goals} | xG: {getattr(row, 'expected_goals', 0)}</p>
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()
                
                config = {'displayModeBar': False}
                
                # 1. Advanced Radar
                st.subheader("Advanced Performance (Radar)")
                fig_radar = go.Figure()
                
                # Define metrics based on availability
                if 'expected_goals' in comp_df.columns:
                    radar_metrics = ['Goals', 'xG', 'Assists', 'xA', 'Prog. Passes', 'Prog. Carries']
                    for row in comp_df.itertuples():
                        values = [row.goals, row.expected_goals, row.assists, row.expected_assists, 
                                  row.progressive_passes/10, row.progressive_carries/10]
                        fig_radar.add_trace(go.Scatterpolar(r=values, theta=radar_metrics, fill='toself', name=row.name))
                else:
                    radar_metrics = ['Rating', 'Goals', 'Assists', 'Key Passes', 'Dribbles', 'Tackles']
                    for row in comp_df.itertuples():
                        values = [row.rating, row.goals, row.assists, row.key_passes/5, row.dribbles/5, row.tackles/5]
                        fig_radar.add_trace(go.Scatterpolar(r=values, theta=radar_metrics, fill='toself', name=row.name))
                
                fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=True)))
                st.plotly_chart(fig_radar, use_container_width=True, theme=None, config=config)

                # 2. Scatter Plot: Efficiency
                st.subheader("Goal Scoring Efficiency (Goals vs xG)")
                if 'expected_goals' in comp_df.columns:
                    fig_scatter = px.scatter(comp_df, x="expected_goals", y="goals", size="progressive_passes", color="name",
                                             hover_data=['name', 'team'], text="name", template="plotly_dark")
                    st.plotly_chart(fig_scatter, use_container_width=True, theme=None, config=config)

            else:
                st.info("Pick players from the loaded rosters to see the magic happen.")
    else:
        st.warning("Click 'Refresh League Data' in the sidebar to load club information.")
