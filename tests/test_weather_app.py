from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from weather_app import (
    Weather,
    WeatherError,
    fetch_weather,
    format_weather,
    weather_emoji,
)


def test_format_weather_metric() -> None:
    weather = Weather(
        city="Istanbul",
        country="TR",
        description="Clear sky",
        temperature=25.5,
        feels_like=26.0,
        humidity=55,
        wind_speed=3.2,
        observed_at=datetime(2026, 8, 25, 10, 30),
    )
    output = format_weather(weather, "metric")
    assert "Istanbul, TR" in output
    assert "25.5°C" in output
    assert "3.2 m/s" in output


def test_clear_day_uses_sun() -> None:
    assert weather_emoji(800, "01d") == "☀️"


def test_rain_uses_rain_emoji() -> None:
    assert weather_emoji(501, "10d") == "🌧️"


def test_clouds_use_cloud_emoji() -> None:
    assert weather_emoji(803, "04d") == "☁️"


def test_malformed_api_payload_raises_weather_error() -> None:
    response = Mock()
    response.json.return_value = {"name": "Istanbul"}
    with patch("weather_app.requests.get", return_value=response):
        with pytest.raises(WeatherError, match="unexpected response"):
            fetch_weather("Istanbul", "test-key")


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Istanbul", "sys": {"country": "TR"}, "weather": [], "main": {}, "wind": {}, "dt": 1},
        {"name": "Istanbul", "sys": {"country": "TR"}, "weather": [{"description": "clear"}],
         "main": {"temp": "not-a-number", "feels_like": 20, "humidity": 50},
         "wind": {"speed": 2}, "dt": 1},
    ],
)
def test_incomplete_or_invalid_numeric_payload_raises_weather_error(payload) -> None:
    response = Mock()
    response.json.return_value = payload
    with patch("weather_app.requests.get", return_value=response):
        with pytest.raises(WeatherError, match="unexpected response"):
            fetch_weather("Istanbul", "test-key")
