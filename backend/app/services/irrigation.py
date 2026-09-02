def irrigation_decision(
    soil_moisture: float,
    temperature: float,
    humidity: float,
    min_moisture: float,
    target_moisture: float
):
    """
    Determine irrigation requirement using
    crop-specific moisture requirements.
    """

    if soil_moisture < min_moisture:
        decision = "ON"
        reason = "Soil moisture is below the crop's minimum requirement."

    elif soil_moisture < target_moisture:
        decision = "OFF"
        reason = "Soil moisture is below target but still above the minimum requirement."

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
        "target_moisture": target_moisture
    }