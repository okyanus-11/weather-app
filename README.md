# Weather Now

A polished Python desktop weather app that fetches live current conditions from [OpenWeatherMap](https://openweathermap.org/api).

## Features

- Desktop GUI built with Python's built-in Tkinter
- Secure API-key field: the key is hidden and never saved
- City search with metric (°C) and imperial (°F) units
- Visual forecast emoji and a clear condition label, such as **Sunny**, **Cloudy**, **Rainy**, **Snowy**, or **Misty**
- Temperature and feels-like temperature
- Humidity, wind, pressure, visibility, sunrise, sunset, and last-updated time
- Friendly messages for invalid keys, unknown cities, timeouts, and network errors
- GitHub Actions test workflow

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Launch

```bash
python weather_app.py
```

Enter your OpenWeatherMap API key and a city, then select **Get weather**.

## API key

Create a free API key in your [OpenWeatherMap account](https://home.openweathermap.org/api_keys). The app does not save your key.

## Test

```bash
pip install pytest
pytest
```

## Security

Never commit an API key. If a key has ever been exposed, revoke it in OpenWeatherMap and create a replacement.

## License

MIT. See [LICENSE](LICENSE).
