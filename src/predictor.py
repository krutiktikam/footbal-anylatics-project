import xgboost as xgb
import os
import pandas as pd

class Predictor:
    def __init__(self, model_path='models/xgboost_model.json'):
        self.model = self._load_model(model_path)
    
    def _load_model(self, model_path):
        if not os.path.exists(model_path):
            print(f"Model not found at {model_path}. Loading fallback...")
            return None
        
        model = xgb.XGBClassifier()
        model.load_model(model_path)
        return model

    def predict(self, df):
        """
        Predict outcomes for the given DataFrame of matches.
        """
        if self.model is None:
            # Fallback to mock if no model exists
            df['HomeWinProbability'] = 0.5
            df['AwayWinProbability'] = 0.5
            return df
        
        # Define the features we used for training
        features = ['Home_Form', 'Away_Form', 'GD_L5']
        
        # Ensure the DataFrame has these features
        if all(f in df.columns for f in features):
            X = df[features]
            # XGBClassifier.predict_proba returns probability for both classes
            probs = self.model.predict_proba(X)
            # Assuming class 1 is Home Win, class 0 is Draw/Away Win
            df['HomeWinProbability'] = probs[:, 1]
            df['AwayWinProbability'] = probs[:, 0]
        else:
            # Fallback if features missing
            df['HomeWinProbability'] = 0.5
            df['AwayWinProbability'] = 0.5
            
        return df
