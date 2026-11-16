# Installation

## Requirements
- Python 3.10 or newer
- An OpenWeatherMap API key
- Internet access

## Windows (PowerShell)

```powershell
git clone https://github.com/okyanus-11/weather-app.git
cd weather-app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `WEATHER_API_KEY` to your OpenWeatherMap API key. Keep this file private; it is ignored by Git.

Run a query:

```powershell
python weather_app.py Istanbul
python weather_app.py "New York" --units imperial
```

Run `python weather_app.py` without a city to enter one interactively.

## Linux / macOS

```bash
git clone https://github.com/okyanus-11/weather-app.git
cd weather-app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Add `WEATHER_API_KEY=your_key_here` to `.env`, then run `python weather_app.py Istanbul`.
