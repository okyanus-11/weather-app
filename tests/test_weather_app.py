from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import requests

from weather_app import Weather, WeatherError, fetch_weather, format_weather


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


def _valid_response() -> dict:
    return {
        "name": "Istanbul",
        "sys": {"country": "TR"},
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25.5, "feels_like": 26.0, "humidity": 55},
        "wind": {"speed": 3.2},
        "dt": 1787653800,
    }


def _fetch_response(payload):
    response = Mock()
    response.json.return_value = payload
    with patch("weather_app.requests.get", return_value=response):
        return fetch_weather("Istanbul", "test-key")


def test_fetch_weather_parses_valid_response() -> None:
    weather = _fetch_response(_valid_response())
    assert weather.city == "Istanbul"
    assert weather.country == "TR"
    assert weather.description == "Clear sky"
    assert weather.temperature == 25.5
    assert weather.humidity == 55


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"name": 1},
        {**_valid_response(), "sys": []},
        {**_valid_response(), "sys": {"country": None}},
        {**_valid_response(), "weather": []},
        {**_valid_response(), "weather": ["clear sky"]},
        {**_valid_response(), "main": []},
        {**_valid_response(), "main": {"temp": "warm", "feels_like": 26, "humidity": 55}},
        {**_valid_response(), "main": {"temp": 25, "feels_like": True, "humidity": 55}},
        {**_valid_response(), "main": {"temp": 25, "feels_like": 26, "humidity": 55.0}},
        {**_valid_response(), "main": {"temp": 25, "feels_like": 26, "humidity": 101}},
        {**_valid_response(), "wind": {"speed": float("nan")}},
        {**_valid_response(), "wind": {"speed": -1}},
        {**_valid_response(), "dt": "1787653800"},
        {**_valid_response(), "dt": 1e100},
    ],
)
def test_fetch_weather_rejects_malformed_response(payload) -> None:
    with pytest.raises(WeatherError, match="unexpected response"):
        _fetch_response(payload)


def test_fetch_weather_rejects_missing_field() -> None:
    payload = _valid_response()
    del payload["main"]["temp"]
    with pytest.raises(WeatherError, match="unexpected response"):
        _fetch_response(payload)


def test_invalid_json_response_has_clear_weather_error() -> None:
    response = Mock()
    response.json.side_effect = requests.exceptions.JSONDecodeError(
        "invalid JSON", "{not-json", 0
    )
    with patch("weather_app.requests.get", return_value=response):
        with pytest.raises(WeatherError, match="invalid JSON"):
            fetch_weather("Istanbul", "test-key")
