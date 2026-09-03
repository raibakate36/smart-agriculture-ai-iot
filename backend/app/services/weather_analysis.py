def analyze_weather(weather_data, forecast_hours=6):
    """
    Analyze the next few hours of weather
    and determine whether rain is expected.
    """

    hourly = weather_data.get("hourly", {})

    probabilities = hourly.get("precipitation_probability", [])
    rain_values = hourly.get("rain", [])

    if not probabilities:
        return {
            "rain_expected": False,
            "rain_probability": 0,
            "forecast_hours": 0,
            "recommendation": "NO_DATA"
        }

    # Look at the next forecast hours
    probabilities = probabilities[:forecast_hours]
    rain_values = rain_values[:forecast_hours]

    max_probability = max(probabilities)

    total_rain = sum(rain_values)

    # Rain is considered likely when probability is >= 60%
    rain_expected = max_probability >= 60

    if rain_expected:
        recommendation = "WAIT"
    else:
        recommendation = "PROCEED"

    return {
        "rain_expected": rain_expected,
        "rain_probability": max_probability,
        "expected_rain_mm": round(total_rain, 2),
        "forecast_hours": len(probabilities),
        "recommendation": recommendation
    }