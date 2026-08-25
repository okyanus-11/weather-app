# Weather App

A lightweight Python command-line app that fetches live current weather from [OpenWeatherMap](https://openweathermap.org/api).

## What it does

1. Securely prompts for an OpenWeatherMap API key (the key is hidden and never saved).
2. Prompts for a city name, or accepts one as a command-line argument.
3. Shows current conditions, temperature, feels-like temperature, humidity, wind, and the observation time.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python weather_app.py
python weather_app.py Istanbul
python weather_app.py "New York" --units imperial
```

Use `metric` (Celsius) by default or pass `--units imperial` for Fahrenheit.

## Get an API key

Create a free API key in your [OpenWeatherMap account](https://home.openweathermap.org/api_keys). The app requests the key every time it runs and does not store it.

## Test

```bash
pip install pytest
pytest
```

## Security

Never commit an API key. If a key has been exposed, revoke it in OpenWeatherMap and issue a replacement.

## License

MIT. See [LICENSE](LICENSE).
