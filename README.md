# Weather App

A command-line app that gets live current weather from OpenWeatherMap.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your key to `.env`, then run:

```powershell
python weather_app.py Istanbul
python weather_app.py "New York" --units imperial
```

Run `python weather_app.py` without a city to enter it interactively.

