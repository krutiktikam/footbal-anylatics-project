from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///football_data.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TeamDB(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    league_id = Column(Integer)
    season = Column(Integer)
    logo = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class PlayerDB(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, index=True)
    season = Column(Integer)
    data = Column(JSON) # Store the Pydantic model data as JSON
    last_updated = Column(DateTime, default=datetime.utcnow)

class FixtureDB(Base):
    __tablename__ = "fixtures"
    fixture_id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, index=True)
    season = Column(Integer)
    data = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions to check cache expiration (e.g., 24 hours)
def is_cache_valid(last_updated, hours=24):
    if not last_updated:
        return False
    return datetime.utcnow() - last_updated < timedelta(hours=hours)
