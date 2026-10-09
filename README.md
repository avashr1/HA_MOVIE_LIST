Home Assistant Movie Library Integration
A lightweight, custom middleware that connects a local SQLite movie database on a Raspberry Pi to a Home Assistant dashboard.

I wanted a way to visualize my local movie collection within my smart home interface without relying on heavy external media server integrations. This project exposes a custom REST API that Home Assistant consumes to generate an interactive, "Netflix-style" swipe card.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your API credentials:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your own tokens:
   - `PUSHBULLET_ACCESS_TOKEN` – from [Pushbullet account settings](https://www.pushbullet.com/#settings/account)
   - `TMDB_API_TOKEN` – the "API Read Access Token" from [TMDB API settings](https://www.themoviedb.org/settings/api)

   `.env` is gitignored, so your secrets stay local.
3. Create the database:
   ```bash
   cd db && python create_db.py
   ```
4. Import movies from Pushbullet and start the API:
   ```bash
   python push.py
   python ha/api.py
   ```
