
from typing import Optional


def generate_recommendation(
    disease: str,
    confidence: float,
    soil_moisture: Optional[float] = None,
    temperature: Optional[float] = None,
    humidity: Optional[float] = None,
    soil_ph: Optional[float] = None,
    nitrogen: Optional[float] = None,
    phosphorus: Optional[float] = None,
    potassium: Optional[float] = None,
):
    """
    Generate tomato crop recommendations using:

    - AI disease prediction
    - AI confidence
    - Soil moisture
    - Temperature
    - Humidity
    - Soil pH
    - NPK sensor readings

    This is decision-support logic for the prototype.
    It does NOT prescribe pesticides or exact fertilizer doses.
    """

    recommendations = []
    nutrient_status = []
    warnings = []

    irrigation = "Insufficient sensor data"

    # =========================================================
    # 1. DISEASE-SPECIFIC RECOMMENDATIONS
    # =========================================================

    disease_lower = disease.lower().strip()

    if disease_lower == "healthy":

        recommendations.append(
            "No visible tomato disease was detected. "
            "Continue regular crop monitoring."
        )

    elif "bacterial_spot" in disease_lower:

        recommendations.append(
            "Bacterial spot detected. Remove severely affected leaves, "
            "avoid overhead irrigation, and monitor nearby plants for spread."
        )

        warnings.append(
            "Avoid spreading contaminated plant material or water between plants."
        )

    elif "early_blight" in disease_lower:

        recommendations.append(
            "Early blight detected. Remove affected leaves, improve air circulation, "
            "and avoid prolonged leaf wetness."
        )

        warnings.append(
            "Avoid unnecessary overhead irrigation because leaf wetness can "
            "encourage disease development."
        )

    elif "late_blight" in disease_lower:

        recommendations.append(
            "Late blight detected. Remove or isolate severely affected plant "
            "material where appropriate and seek agricultural treatment advice promptly."
        )

        warnings.append(
            "Late blight can spread rapidly under favorable conditions. "
            "Monitor nearby plants closely."
        )

    elif "leaf_mold" in disease_lower:

        recommendations.append(
            "Leaf mold detected. Improve ventilation, reduce excessive humidity, "
            "and avoid prolonged leaf wetness."
        )

    elif "septoria" in disease_lower:

        recommendations.append(
            "Septoria leaf spot detected. Remove infected foliage, improve airflow, "
            "and avoid splashing water onto leaves."
        )

    elif "spider_mites" in disease_lower:

        recommendations.append(
            "Spider mites detected. Inspect the underside of leaves and monitor "
            "the crop closely for increasing mite activity."
        )

        warnings.append(
            "Check multiple plants because mite infestations can spread through the crop."
        )

    elif "target_spot" in disease_lower:

        recommendations.append(
            "Target spot detected. Remove heavily affected foliage, improve "
            "air circulation, and avoid prolonged leaf wetness."
        )

    elif "mosaic_virus" in disease_lower:

        recommendations.append(
            "Tomato mosaic virus detected. Remove infected plants where appropriate "
            "and prevent contamination through tools and plant handling."
        )

        warnings.append(
            "Disinfect tools and avoid handling healthy plants immediately after "
            "handling infected plants."
        )

    elif "yellow_leaf_curl" in disease_lower:

        recommendations.append(
            "Tomato yellow leaf curl virus detected. Monitor and manage its "
            "insect vector according to local agricultural guidance."
        )

        warnings.append(
            "Inspect plants for signs of vector activity and monitor nearby plants."
        )

    else:

        recommendations.append(
            "Unknown condition detected. Further inspection is recommended."
        )

    # =========================================================
    # 2. AI CONFIDENCE
    # =========================================================

    if confidence < 50:

        warnings.append(
            "AI confidence is low. Upload a clearer image or verify the result "
            "with an agricultural expert before taking action."
        )

    elif confidence < 70:

        warnings.append(
            "AI confidence is moderate. Consider verifying the result with "
            "another clear image or expert inspection."
        )

    elif confidence >= 95:

        recommendations.append(
            "AI confidence is very high, but visual diagnosis should still be "
            "combined with field observation and sensor information."
        )

    # =========================================================
    # 3. IRRIGATION
    # =========================================================

    if soil_moisture is not None:

        if soil_moisture < 20:

            irrigation = (
                "Soil moisture is very low. Irrigation may be required soon."
            )

        elif soil_moisture < 30:

            irrigation = (
                "Soil moisture is low. Consider irrigation and continue monitoring."
            )

        elif soil_moisture < 40:

            irrigation = (
                "Soil moisture is moderate. Monitor moisture closely."
            )

        elif soil_moisture <= 70:

            irrigation = (
                "Soil moisture is in a generally adequate range. "
                "Avoid unnecessary irrigation."
            )

        else:

            irrigation = (
                "Soil moisture is high. Avoid unnecessary irrigation and "
                "monitor drainage."
            )

    # =========================================================
    # 4. TEMPERATURE
    # =========================================================

    if temperature is not None:

        if temperature > 35:

            recommendations.append(
                "High temperature detected. Monitor the crop for heat stress "
                "and maintain adequate soil moisture."
            )

        elif temperature > 32:

            recommendations.append(
                "Temperature is relatively high. Monitor plants for heat stress "
                "and check soil moisture regularly."
            )

        elif temperature < 15:

            recommendations.append(
                "Low temperature detected. Monitor the crop for cold stress."
            )

    # =========================================================
    # 5. HUMIDITY
    # =========================================================

    if humidity is not None:

        if humidity > 85:

            recommendations.append(
                "Very high humidity detected. Improve airflow and avoid "
                "unnecessary leaf wetness because humid conditions can favor "
                "several fungal diseases."
            )

        elif humidity > 75:

            recommendations.append(
                "Humidity is relatively high. Improve ventilation and monitor "
                "the foliage for disease symptoms."
            )

        elif humidity < 30:

            recommendations.append(
                "Humidity is low. Monitor plants for water stress, especially "
                "during high temperatures."
            )

    # =========================================================
    # 6. SOIL pH
    # =========================================================

    if soil_ph is not None:

        if soil_ph < 5.5:

            nutrient_status.append(
                "Soil pH is acidic."
            )

            warnings.append(
                "Consider soil testing and appropriate agricultural guidance "
                "before making pH amendments."
            )

        elif soil_ph > 7.5:

            nutrient_status.append(
                "Soil pH is alkaline."
            )

            warnings.append(
                "Consider soil testing and appropriate agricultural guidance "
                "before making pH amendments."
            )

        else:

            nutrient_status.append(
                "Soil pH is within a suitable monitoring range."
            )

    # =========================================================
    # 7. NITROGEN
    # =========================================================

    if nitrogen is not None:

        if nitrogen < 30:

            nutrient_status.append(
                "Nitrogen level appears low."
            )

            warnings.append(
                "Consider confirming nitrogen status with a soil test "
                "before applying fertilizer."
            )

        elif nitrogen > 150:

            nutrient_status.append(
                "Nitrogen level appears high."
            )

            warnings.append(
                "Avoid unnecessary nitrogen application until the reading "
                "is verified."
            )

        else:

            nutrient_status.append(
                "Nitrogen level appears adequate."
            )

    # =========================================================
    # 8. PHOSPHORUS
    # =========================================================

    if phosphorus is not None:

        if phosphorus < 20:

            nutrient_status.append(
                "Phosphorus level appears low."
            )

        elif phosphorus > 100:

            nutrient_status.append(
                "Phosphorus level appears high."
            )

        else:

            nutrient_status.append(
                "Phosphorus level appears adequate."
            )

    # =========================================================
    # 9. POTASSIUM
    # =========================================================

    if potassium is not None:

        if potassium < 30:

            nutrient_status.append(
                "Potassium level appears low."
            )

        elif potassium > 200:

            nutrient_status.append(
                "Potassium level appears high."
            )

        else:

            nutrient_status.append(
                "Potassium level appears adequate."
            )

    # =========================================================
    # 10. COMBINATION-BASED CONDITIONS
    # =========================================================

    # High humidity + fungal-type diseases
    fungal_diseases = (
        "early_blight",
        "late_blight",
        "leaf_mold",
        "septoria",
        "target_spot",
    )

    if (
        any(d in disease_lower for d in fungal_diseases)
        and humidity is not None
        and humidity > 75
    ):

        recommendations.append(
            "The detected disease and current humidity conditions may increase "
            "the risk of disease development. Prioritize airflow and keep foliage dry."
        )

    # High temperature + low soil moisture
    if (
        temperature is not None
        and temperature > 32
        and soil_moisture is not None
        and soil_moisture < 30
    ):

        recommendations.append(
            "High temperature combined with low soil moisture may increase "
            "plant water stress. Monitor the crop closely and consider irrigation."
        )

    # Excessive moisture + high humidity
    if (
        soil_moisture is not None
        and soil_moisture > 70
        and humidity is not None
        and humidity > 80
    ):

        warnings.append(
            "Both soil moisture and humidity are high. Avoid unnecessary irrigation "
            "and monitor the crop for disease-favorable conditions."
        )

    # =========================================================
    # 11. SENSOR DATA STATUS
    # =========================================================

    sensor_values = [
        soil_moisture,
        temperature,
        humidity,
        soil_ph,
        nitrogen,
        phosphorus,
        potassium,
    ]

    available_sensor_count = sum(
        value is not None for value in sensor_values
    )

    if available_sensor_count == 0:

        warnings.append(
            "No sensor readings were available. Recommendations are based mainly "
            "on the image diagnosis."
        )

    elif available_sensor_count < len(sensor_values):

        warnings.append(
            f"Only {available_sensor_count} of {len(sensor_values)} sensor "
            "parameters were available."
        )

    # =========================================================
    # FINAL RESULT
    # =========================================================

    return {
        "disease": disease,
        "confidence": round(float(confidence), 2),

        "irrigation": irrigation,

        "nutrient_status": nutrient_status,

        "recommendations": recommendations,

        "warnings": warnings,

        "sensor_parameters_available": available_sensor_count,
    }

