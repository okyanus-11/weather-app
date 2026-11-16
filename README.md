## Weather App

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

## Installation

Requires Python 3.10+ and an OpenWeatherMap API key. Clone the repository, create a virtual environment, install `requirements.txt`, copy `.env.example` to `.env`, and add `WEATHER_API_KEY`. Start it with `python weather_app.py Istanbul` (or omit the city for interactive input). See the [full installation guide](INSTALLATION.md) for Windows and Linux/macOS steps.
