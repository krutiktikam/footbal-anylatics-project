import xgboost as xgb
import pandas as pd
import os
from src.data_ingestion import fetch_historical_fixtures
from src.preprocessing import process_fixtures_to_df, engineer_features

def train_xgboost_model(league_id=39, season=2023):
    """
    Fetches data, engineers features, trains XGBoost, and saves it.
    """
    print(f"Fetching historical data for league {league_id}, season {season}...")
    fixtures_json = fetch_historical_fixtures(league_id, season, last_n=50)
    
    if not fixtures_json:
        print("No historical data found. Creating synthetic training data...")
        # Synthetic data for demonstration if API fails/has no results
        data = {
            'Home_Form': [2.5, 1.0, 3.0, 0.5, 2.0] * 10,
            'Away_Form': [1.5, 2.0, 0.5, 3.0, 1.0] * 10,
            'GD_L5': [5, -2, 8, -5, 2] * 10,
            'Target': [1, 0, 1, 0, 1] * 10 # 1: Home Win, 0: Draw/Away Win
        }
        df = pd.DataFrame(data)
    else:
        df = process_fixtures_to_df(fixtures_json)
        # Add target label: 1 if Home goals > Away goals, else 0
        df['Target'] = (df['home_goals'] > df['away_goals']).astype(int)
        df = engineer_features(df)
    
    # Define features and target
    features = ['Home_Form', 'Away_Form', 'GD_L5']
    X = df[features]
    y = df['Target']
    
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X, y)
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    model.save_model('models/xgboost_model.json')
    print("Model saved to models/xgboost_model.json")

if __name__ == "__main__":
    train_xgboost_model()
