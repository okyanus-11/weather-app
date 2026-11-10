from datetime import datetime
from typing import Any

import pytest

from weather_app import Weather, WeatherError, fetch_weather, format_weather


def _valid_response() -> dict[str, Any]:
    return {
        "name": "Istanbul",
        "sys": {"country": "TR"},
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25.5, "feels_like": 26.0, "humidity": 55},
        "wind": {"speed": 3.2},
        "dt": 1787653800,
    }


def _fetch_response(monkeypatch: pytest.MonkeyPatch, payload: Any) -> Weather:
    class Response:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> Any:
            return payload

    monkeypatch.setattr("weather_app.requests.get", lambda *args, **kwargs: Response())
    return fetch_weather("Istanbul", "test-key")


def test_format_weather_metric() -> None:
    weather = Weather("Istanbul", "TR", "Clear sky", 25.5, 26.0, 55, 3.2, datetime(2026, 8, 25, 10, 30))
    output = format_weather(weather, "metric")
    assert "Istanbul, TR" in output
    assert "25.5°C" in output
    assert "3.2 m/s" in output


def test_fetch_weather_parses_valid_response(monkeypatch: pytest.MonkeyPatch) -> None:
    weather = _fetch_response(monkeypatch, _valid_response())

    assert weather.city == "Istanbul"
    assert weather.country == "TR"
    assert weather.description == "Clear sky"
    assert weather.temperature == 25.5


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ((), []),
        (("name",), 1),
        (("sys",), []),
        (("sys", "country"), None),
        (("weather",), []),
        (("weather", 0), "clear sky"),
        (("weather", 0, "description"), 1),
        (("main",), []),
        (("main", "temp"), "warm"),
        (("main", "feels_like"), True),
        (("main", "humidity"), 55.0),
        (("wind",), []),
        (("wind", "speed"), None),
        (("dt",), "1787653800"),
        (("dt",), 1e100),
    ],
)
def test_fetch_weather_rejects_malformed_response(
    monkeypatch: pytest.MonkeyPatch, path: tuple[object, ...], value: object
) -> None:
    payload: Any = _valid_response()
    if path:
        target = payload
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    else:
        payload = value

    with pytest.raises(WeatherError, match="unexpected response"):
        _fetch_response(monkeypatch, payload)


def test_fetch_weather_rejects_missing_field(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_response()
    del payload["main"]["temp"]

    with pytest.raises(WeatherError, match="unexpected response"):
        _fetch_response(monkeypatch, payload)
