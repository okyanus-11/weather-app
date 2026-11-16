from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from weather_app import Weather, WeatherError, fetch_weather, format_weather


def test_format_weather_metric() -> None:
    weather = Weather("Istanbul", "TR", "Clear sky", 25.5, 26.0, 55, 3.2, datetime(2026, 8, 25, 10, 30))
    output = format_weather(weather, "metric")
    assert "Istanbul, TR" in output
    assert "25.5°C" in output
    assert "3.2 m/s" in output


def test_malformed_api_payload_raises_weather_error() -> None:
    response = Mock()
    response.json.return_value = {"name": "Istanbul"}
    with patch("weather_app.requests.get", return_value=response):
        with pytest.raises(WeatherError, match="unexpected response"):
            fetch_weather("Istanbul", "test-key")
