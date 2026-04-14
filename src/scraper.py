import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from .models import PlayerStats

class FBRefScraper:
    BASE_URL = "https://fbref.com"

    def get_league_url(self, league_name):
        leagues = {
            'Premier League': "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
            'La Liga': "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
            'Bundesliga': "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
            'Serie A': "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
            'Ligue 1': "https://fbref.com/en/comps/13/stats/Ligue-1-Stats"
        }
        return leagues.get(league_name)

    def scrape_players_by_league(self, league_name):
        url = self.get_league_url(league_name)
        if not url:
            return []

        print(f"Scraping {league_name} from FBRef...")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # FBRef usually keeps stats in a 'stats_standard' table
        table = soup.find('table', {'id': 'stats_standard'})
        if not table:
            return []

        df = pd.read_html(str(table))[0]
        # Drop multi-index if it exists
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(0)

        # Cleanup: Remove rows that repeat headers
        df = df[df['Player'] != 'Player']
        
        players_list = []
        for index, row in df.iterrows():
            try:
                # FBRef uses npxG (non-penalty xG) and xG
                p_stats = PlayerStats(
                    name=row['Player'],
                    team=row['Squad'],
                    age=int(str(row['Age']).split('-')[0]) if pd.notna(row['Age']) else 0,
                    nationality=row['Nation'].split(' ')[-1] if pd.notna(row['Nation']) else "N/A",
                    rating=0.0, # FBRef doesn't have a single "Rating" like the API
                    goals=int(row['Gls']) if pd.notna(row['Gls']) else 0,
                    assists=int(row['Ast']) if pd.notna(row['Ast']) else 0,
                    expected_goals=float(row['xG']) if pd.notna(row['xG']) else 0.0,
                    expected_assists=float(row['xAG']) if pd.notna(row['xAG']) else 0.0,
                    progressive_passes=int(row['PrgP']) if pd.notna(row['PrgP']) else 0,
                    progressive_carries=int(row['PrgC']) if pd.notna(row['PrgC']) else 0
                )
                players_list.append(p_stats.model_dump())
            except Exception as e:
                # Silently skip errors for now
                continue

        return players_list
