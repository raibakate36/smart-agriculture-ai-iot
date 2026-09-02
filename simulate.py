import requests
import time
import random

# ============================================================
# SMART AGRICULTURE - REALISTIC VIRTUAL IoT SIMULATOR
# ============================================================

API_URL = "http://127.0.0.1:8000/api/v1/sensor-data"

DEVICE_ID = "FIELD_001"
CROP = "tomato"

# ------------------------------------------------------------
# Initial field conditions
# ------------------------------------------------------------

soil_moisture = 40.0
temperature = 30.0
humidity = 65.0
soil_ph = 6.4

nitrogen = 50.0
phosphorus = 45.0
potassium = 60.0

# Crop irrigation limits
MIN_MOISTURE = 25.0
TARGET_MOISTURE = 40.0


# ============================================================
# GENERATE REALISTIC SENSOR CHANGES
# ============================================================

def update_environment():

    global soil_moisture
    global temperature
    global humidity
    global soil_ph
    global nitrogen
    global phosphorus
    global potassium

    # --------------------------------------------------------
    # Soil moisture naturally decreases over time
    # --------------------------------------------------------

    soil_moisture -= random.uniform(1.0, 3.0)

    # --------------------------------------------------------
    # Simulate irrigation
    #
    # If soil becomes too dry, irrigation turns ON.
    # --------------------------------------------------------

    irrigation_on = False

    if soil_moisture < MIN_MOISTURE:

        irrigation_on = True

        print("\n💧 IRRIGATION ON")
        print("Soil moisture is below minimum requirement.")

        # Simulate water being supplied
        soil_moisture += random.uniform(8.0, 12.0)

    # --------------------------------------------------------
    # Gradual environmental changes
    # --------------------------------------------------------

    temperature += random.uniform(-1.0, 1.0)

    humidity += random.uniform(-2.0, 2.0)

    soil_ph += random.uniform(-0.05, 0.05)

    nitrogen -= random.uniform(0.1, 0.5)

    phosphorus -= random.uniform(0.05, 0.3)

    potassium -= random.uniform(0.1, 0.4)

    # --------------------------------------------------------
    # Keep values within realistic ranges
    # --------------------------------------------------------

    soil_moisture = max(10, min(80, soil_moisture))

    temperature = max(20, min(38, temperature))

    humidity = max(40, min(90, humidity))

    soil_ph = max(5.0, min(8.0, soil_ph))

    nitrogen = max(10, nitrogen)

    phosphorus = max(10, phosphorus)

    potassium = max(10, potassium)

    return irrigation_on


# ============================================================
# SEND SENSOR DATA TO FASTAPI
# ============================================================

def send_sensor_data():

    irrigation_on = update_environment()

    data = {
        "device_id": DEVICE_ID,
        "crop": CROP,

        "soil_moisture": round(soil_moisture, 2),

        "temperature": round(temperature, 2),

        "humidity": round(humidity, 2),

        "soil_ph": round(soil_ph, 2),

        "nitrogen": round(nitrogen, 2),

        "phosphorus": round(phosphorus, 2),

        "potassium": round(potassium, 2),
    }

    print("\n" + "=" * 60)
    print("🌱 VIRTUAL TOMATO FIELD")
    print("=" * 60)

    print(f"Device        : {DEVICE_ID}")
    print(f"Crop          : {CROP}")

    print(f"Soil Moisture : {data['soil_moisture']}%")

    print(f"Temperature   : {data['temperature']} °C")

    print(f"Humidity      : {data['humidity']}%")

    print(f"Soil pH       : {data['soil_ph']}")

    print(f"Nitrogen      : {data['nitrogen']}")

    print(f"Phosphorus    : {data['phosphorus']}")

    print(f"Potassium     : {data['potassium']}")

    if irrigation_on:
        print("Irrigation    : ON 💧")
    else:
        print("Irrigation    : OFF")

    # --------------------------------------------------------
    # Send to FastAPI
    # --------------------------------------------------------

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        if response.status_code == 200:

            print("\n✅ Sensor data sent successfully")

            print(
                f"Database ID: "
                f"{response.json().get('id')}"
            )

        else:

            print("\n❌ Backend returned error")

            print(response.status_code)

            print(response.text)

    except requests.exceptions.ConnectionError:

        print("\n❌ Cannot connect to FastAPI.")

        print(
            "Make sure the backend is running on "
            "http://127.0.0.1:8000"
        )

    except Exception as e:

        print(f"\n❌ Error: {e}")


# ============================================================
# START SIMULATION
# ============================================================

print("=" * 60)
print("🌱 SMART AGRICULTURE")
print("REALISTIC VIRTUAL IoT SENSOR")
print("=" * 60)

print()

print("Device:", DEVICE_ID)
print("Crop:", CROP)

print()

print("Simulation started.")

print("Press CTRL+C to stop.")

print()

# ============================================================
# CONTINUOUS SIMULATION
# ============================================================

while True:

    send_sensor_data()

    # Wait 10 seconds before next reading
    time.sleep(10)