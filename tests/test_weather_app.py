from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import requests

from weather_app import (
    Weather,
    WeatherError,
    fetch_weather,
    format_weather,
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


def test_fetch_weather_parses_valid_response() -> None:
    response = Mock()
    response.json.return_value = {
        "name": "Istanbul",
        "sys": {"country": "TR"},
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 22, "feels_like": 23, "humidity": 48},
        "wind": {"speed": 3.5},
        "dt": 1798209000,
    }
    with patch("weather_app.requests.get", return_value=response):
        weather = fetch_weather("Istanbul", "test-key")
    assert weather.city == "Istanbul"
    assert weather.country == "TR"
    assert weather.description == "Clear sky"
    assert weather.temperature == 22.0
    assert weather.humidity == 48


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

def test_invalid_json_response_has_clear_weather_error() -> None:
    response = Mock()
    response.json.side_effect = requests.exceptions.JSONDecodeError(
        "invalid JSON", "{not-json", 0
    )
    with patch("weather_app.requests.get", return_value=response):
        with pytest.raises(WeatherError, match="invalid JSON"):
            fetch_weather("Istanbul", "test-key")
