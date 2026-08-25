"""Command-line weather app powered by OpenWeatherMap."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from getpass import getpass
from typing import Any

import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherError(RuntimeError):
    """Raised when OpenWeatherMap cannot provide weather data."""


@dataclass(frozen=True)
class Weather:
    city: str
    country: str
    description: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    observed_at: datetime


def fetch_weather(city: str, api_key: str, units: str = "metric") -> Weather:
    """Fetch current conditions for a city from OpenWeatherMap."""
    try:
        response = requests.get(
            API_URL,
            params={"q": city, "appid": api_key, "units": units},
            timeout=10,
        )
        response.raise_for_status()
    except requests.Timeout as error:
        raise WeatherError("The weather service took too long to respond. Please try again.") from error
    except requests.RequestException as error:
        raise WeatherError(_error_message(error)) from error

    data: dict[str, Any] = response.json()
    return Weather(
        city=data["name"],
        country=data["sys"]["country"],
        description=data["weather"][0]["description"].capitalize(),
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        observed_at=datetime.fromtimestamp(data["dt"]),
    )


def _error_message(error: requests.RequestException) -> str:
    """Turn API errors into helpful user-facing messages."""
    if error.response is None:
        return "Could not reach OpenWeatherMap. Check your internet connection."
    if error.response.status_code == 401:
        return "Your OpenWeatherMap API key was rejected. Check the key and try again."
    if error.response.status_code == 404:
        return "City not found. Try a city and country code, such as 'London,GB'."
    return f"OpenWeatherMap returned an error ({error.response.status_code}). Please try again."


def format_weather(weather: Weather, units: str) -> str:
    """Format conditions into a readable terminal card."""
    temperature_unit = "°F" if units == "imperial" else "°C"
    wind_unit = "mph" if units == "imperial" else "m/s"
    return (
        f"\nCurrent weather — {weather.city}, {weather.country}\n"
        f"{'─' * 38}\n"
        f"Condition:    {weather.description}\n"
        f"Temperature:  {weather.temperature:.1f}{temperature_unit}\n"
        f"Feels like:   {weather.feels_like:.1f}{temperature_unit}\n"
        f"Humidity:     {weather.humidity}%\n"
        f"Wind:         {weather.wind_speed:.1f} {wind_unit}\n"
        f"Updated:      {weather.observed_at:%Y-%m-%d %H:%M}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get live weather from OpenWeatherMap.")
    parser.add_argument("city", nargs="?", help="City name, e.g. Istanbul or London,GB")
    parser.add_argument("--units", choices=("metric", "imperial"), default="metric")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = getpass("OpenWeatherMap API key (hidden): ").strip()
    city = args.city or input("City: ").strip()

    if not api_key:
        print("An OpenWeatherMap API key is required.", file=sys.stderr)
        return 2
    if not city:
        print("Please provide a city name.", file=sys.stderr)
        return 2

    try:
        weather = fetch_weather(city, api_key, args.units)
    except WeatherError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(format_weather(weather, args.units))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
