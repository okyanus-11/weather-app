from weather_app import weather_emoji


def test_clear_day_uses_sun() -> None:
    assert weather_emoji(800, "01d") == "☀️"


def test_rain_uses_rain_emoji() -> None:
    assert weather_emoji(501, "10d") == "🌧️"


def test_clouds_use_cloud_emoji() -> None:
    assert weather_emoji(803, "04d") == "☁️"
