def irrigation_decision(
    soil_moisture: float,
    temperature: float,
    humidity: float,
    min_moisture: float,
    target_moisture: float,
    rain_probability: float = 0,
    expected_rain_mm: float = 0
):
    """
    Determine irrigation requirement using
    crop-specific moisture requirements and
    upcoming rainfall forecast.
    """

    # Soil is critically dry
    if soil_moisture < min_moisture:

        # Rain is likely, so wait before irrigating
        if rain_probability >= 60:
            decision = "WAIT"
            reason = (
                "Soil moisture is below the crop's minimum requirement, "
                "but significant rainfall is expected soon."
            )

        # Rain is unlikely, so irrigation can proceed
        else:
            decision = "ON"
            reason = (
                "Soil moisture is below the crop's minimum requirement "
                "and rainfall is unlikely."
            )

    # Soil is below target but not critically dry
    elif soil_moisture < target_moisture:
        decision = "OFF"
        reason = (
            "Soil moisture is below target but still above "
            "the minimum requirement."
        )

    # Soil has sufficient moisture
    else:
        decision = "OFF"
        reason = "Soil moisture is sufficient."

    return {
        "irrigation": decision,
        "reason": reason,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "min_moisture": min_moisture,
        "target_moisture": target_moisture,
        "rain_probability": rain_probability,
        "expected_rain_mm": expected_rain_mm
    }