from datetime import datetime

from weather_app import Weather, format_weather


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
