# 🛰️ Football Data Engine: Independent Harvester Roadmap

*Goal: Create a resilient, automated pipeline to feed high-quality data into our cloud store.*

## 🛠️ Phase 1: Cloud Store Setup (Current)
- [ ] **Supabase Provisioning:** Setup a free-tier PostgreSQL instance on Supabase.
- [ ] **Schema Migration:** Create optimized tables for `scraped_players`, `team_stats`, and `league_standings`.
- [ ] **Connection Layer:** Build a secure DB adapter in Python using `SQLAlchemy`.

## 🕷️ Phase 2: Resilient Scraper Development
- [ ] **FBRef Historical Scraper:** Scrape data for the last 5 seasons to enable "Trend Analysis."
- [ ] **SofaScore Live Scraper:** Use `Playwright` to handle dynamic JavaScript content for live match ratings.
- [ ] **Proxy & User-Agent Rotation:** Implement measures to prevent IP blocking from FBRef/SofaScore.

## 🤖 Phase 3: Automation (The "Set & Forget")
- [ ] **GitHub Actions Cron:** Schedule the scraper to run every night at 3 AM.
- [ ] **Data Cleaning Pipeline:** Automated script to handle "Player Name Normalization" (e.g., matching "L. Messi" in the API to "Lionel Messi" in the Scraper).
- [ ] **Health Checks:** Send a Telegram/Discord notification if a scraping run fails.

## 🔌 Phase 4: Unified API (Optional)
- [ ] **Data Engine API:** A tiny FastAPI service that acts as the single source of truth for our Comparison App.
