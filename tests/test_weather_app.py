from datetime import datetime

from weather_app import Weather, format_weather


def test_format_weather_metric() -> None:
    weather = Weather("Istanbul", "TR", "Clear sky", 25.5, 26.0, 55, 3.2, datetime(2026, 8, 25, 10, 30))
    output = format_weather(weather, "metric")
    assert "Istanbul, TR" in output
    assert "25.5°C" in output
    assert "3.2 m/s" in output

