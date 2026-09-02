def analyze_tomato_condition(
    soil_moisture: float,
    temperature: float,
    humidity: float,
    soil_ph: float | None = None,
    nitrogen: float | None = None,
    phosphorus: float | None = None,
    potassium: float | None = None,
    image_condition: str | None = None,
):
    """
    Temporary tomato crop-health decision layer.

    This will later be connected to the trained ML models.
    """

    warnings = []
    recommendations = []

    # -----------------------------
    # Soil moisture
    # -----------------------------
    if soil_moisture < 25:
        warnings.append("Low soil moisture")
        recommendations.append("Irrigation may be required.")

    elif soil_moisture > 80:
        warnings.append("High soil moisture")
        recommendations.append("Avoid excessive irrigation.")

    # -----------------------------
    # Temperature
    # -----------------------------
    if temperature > 35:
        warnings.append("High temperature")
        recommendations.append("Monitor heat stress.")

    elif temperature < 15:
        warnings.append("Low temperature")
        recommendations.append("Monitor cold stress.")

    # -----------------------------
    # Humidity
    # -----------------------------
    if humidity > 80:
        warnings.append("High humidity")
        recommendations.append(
            "Monitor the crop for fungal disease symptoms."
        )

    # -----------------------------
    # Soil pH
    # -----------------------------
    if soil_ph is not None:

        if soil_ph < 5.5:
            warnings.append("Soil pH is low")

        elif soil_ph > 7.5:
            warnings.append("Soil pH is high")

    # -----------------------------
    # Image condition
    # -----------------------------
    if image_condition:

        if image_condition.lower() != "healthy":
            warnings.append(
                f"Image analysis indicates: {image_condition}"
            )

    # -----------------------------
    # Overall status
    # -----------------------------
    if not warnings:
        status = "NORMAL"

    elif len(warnings) == 1:
        status = "ATTENTION"

    else:
        status = "WARNING"

    return {
        "crop": "tomato",
        "status": status,
        "warnings": warnings,
        "recommendations": recommendations,
    }