# football-prediction-pro ⚽

A professional, scalable pipeline for live football predictions using XGBoost and Streamlit.

## Project Structure
- `data/`: Placeholder for datasets.
- `models/`: Store your trained XGBoost models (`xgboost_model.json`).
- `notebooks/`: For experimental analysis and model training.
- `src/`: Core logic for data ingestion, preprocessing, and prediction.
- `app/`: Streamlit dashboard application.

## Getting Started

### 1. Setup Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root directory and add your [API-Football](https://api-sports.io/documentation/football/v3) key:
```
FOOTBALL_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
streamlit run app/main.py
```

## How it works
1. **Data Ingestion**: Fetches live fixtures from the API based on the selected league.
2. **Preprocessing**: Transforms raw JSON into a structured DataFrame.
3. **Prediction**: Loads your pre-trained XGBoost model and calculates win probabilities.
4. **Dashboard**: Displays a live table of upcoming match results and predictions.
