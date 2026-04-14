
import sys
import os
from datetime import datetime

# Add src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import engine, SessionLocal, TeamDB
from src.models import Team, PlayerStats

def test_phase_1():
    print("🔍 Testing Phase 1: Data Foundation...")
    
    # 1. Test Database Connection
    try:
        db = SessionLocal()
        print("✅ Database connection successful.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    # 2. Test Pydantic Validation
    try:
        valid_player = PlayerStats(
            name="L. Messi",
            team="Inter Miami",
            rating=8.5,
            goals=10
        )
        print(f"✅ Pydantic Validation successful: {valid_player.name}")
    except Exception as e:
        print(f"❌ Pydantic Validation failed: {e}")

    # 3. Test Database Insertion (Mock Team)
    try:
        mock_team = TeamDB(
            id=9999,
            name="Test FC",
            league_id=39,
            season=2024,
            last_updated=datetime.utcnow()
        )
        db.merge(mock_team)
        db.commit()
        print("✅ Database Record Insertion (Caching Logic) successful.")
    except Exception as e:
        print(f"❌ Database Insertion failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_phase_1()
