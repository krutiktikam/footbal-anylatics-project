from pydantic import BaseModel, Field
from typing import Optional, List

# --- Team Models ---
class Team(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[int] = None

# --- Player Models ---
class PlayerStats(BaseModel):
    name: str
    team: str
    age: Optional[int] = None
    nationality: Optional[str] = None
    rating: float = 0.0
    
    # Basic Stats
    goals: int = 0
    assists: int = 0
    shots: int = 0
    passes: int = 0
    key_passes: int = 0
    tackles: int = 0
    interceptions: int = 0
    dribbles: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    
    # --- Phase 1.5: Advanced Scraped Stats ---
    expected_goals: Optional[float] = Field(default=0.0, alias="xG")
    expected_assists: Optional[float] = Field(default=0.0, alias="xA")
    progressive_passes: Optional[int] = 0
    progressive_carries: Optional[int] = 0
    touches_in_box: Optional[int] = 0
    pressures: Optional[int] = 0

    class Config:
        populate_by_name = True

# --- Fixture Models ---
class Fixture(BaseModel):
    fixture_id: int
    home_team: str
    away_team: str
    home_team_id: int
    away_team_id: int
    league_id: int
    season: int
    home_win_probability: Optional[float] = None
    away_win_probability: Optional[float] = None
