\# 🌱 Smart Agriculture AI \& IoT



An AI and IoT-based smart agriculture system designed for \*\*tomato crop monitoring, disease detection, automated irrigation, and intelligent crop-health recommendations\*\*.



The system combines artificial intelligence, IoT sensors, weather information, and a mobile application to help farmers make better decisions about their crops.



\---



\## 🚀 Features



\### 🍅 AI-Based Disease Detection



\* Upload a tomato leaf image.

\* EfficientNet-B0 based deep-learning model analyzes the image.

\* Detects common tomato leaf diseases.

\* Provides prediction confidence and top predictions.

\* Generates disease-specific recommendations.



\### 📡 IoT-Based Crop Monitoring



The system collects environmental and soil parameters such as:



\* Soil moisture

\* Temperature

\* Humidity

\* Soil pH

\* Nitrogen (N)

\* Phosphorus (P)

\* Potassium (K)



The planned hardware platform is \*\*ESP32\*\* with appropriate sensors.



\### 💧 Automated Irrigation



The system analyzes soil moisture and crop requirements to determine whether irrigation is required.



Example:



```text

Soil moisture < minimum threshold

&#x20;       ↓

Irrigation required

&#x20;       ↓

Pump ON

```



When sufficient moisture is reached:



```text

Soil moisture ≥ target level

&#x20;       ↓

Irrigation not required

&#x20;       ↓

Pump OFF

```



\### 🌱 Crop Health Analysis



The system combines sensor information and AI results to provide:



\* Crop health status

\* Warnings

\* Irrigation recommendations

\* Nutrient status

\* Disease-specific recommendations



\### 🌦️ Weather-Aware Agriculture



Weather information will be incorporated into the decision-making system to help avoid unnecessary irrigation and provide weather-related crop recommendations.



\### 📱 Mobile Application



A mobile application is being developed as the main interface for farmers.



Planned sections include:



\* Dashboard

\* Disease Detection

\* Irrigation

\* Crop Health

\* Weather

\* Sensor Monitoring

\* Historical Data



\---



\# 🏗️ System Architecture



```text

&#x20;                        🌱 TOMATO CROP

&#x20;                             │

&#x20;             ┌───────────────┴───────────────┐

&#x20;             │                               │

&#x20;             ▼                               ▼

&#x20;      📡 IoT Sensors                    📷 Leaf Image

&#x20;             │                               │

&#x20;             ▼                               ▼

&#x20;           ESP32                       AI Disease Model

&#x20;             │                               │

&#x20;             └───────────────┬───────────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                      🌐 FastAPI Backend

&#x20;                             │

&#x20;             ┌───────────────┼───────────────┐

&#x20;             │               │               │

&#x20;             ▼               ▼               ▼

&#x20;         🧠 AI Model      💧 Irrigation    🌦️ Weather

&#x20;             │               │               │

&#x20;             └───────────────┼───────────────┘

&#x20;                             ▼

&#x20;                   🧠 Decision Engine

&#x20;                             │

&#x20;                             ▼

&#x20;                        📱 Mobile App

&#x20;                             │

&#x20;                             ▼

&#x20;                        👨‍🌾 Farmer

```



\---



\# 🔄 System Workflow



```text

1\. Sensors collect field data

&#x20;             ↓

2\. ESP32 sends data to backend

&#x20;             ↓

3\. Backend stores sensor readings

&#x20;             ↓

4\. Farmer uploads tomato leaf image

&#x20;             ↓

5\. AI model predicts disease

&#x20;             ↓

6\. Decision engine combines:

&#x20;     • Disease prediction

&#x20;     • Soil conditions

&#x20;     • Environmental conditions

&#x20;     • Weather information

&#x20;             ↓

7\. System generates recommendations

&#x20;             ↓

8\. Mobile application displays results

```



\---



\# 🧠 Machine Learning



The project uses \*\*EfficientNet-B0\*\* for tomato leaf disease classification.



The ML pipeline contains:



```text

Dataset

&#x20;  ↓

Data Preparation

&#x20;  ↓

Training

&#x20;  ↓

Evaluation

&#x20;  ↓

Trained Model

&#x20;  ↓

Prediction

```



ML development files are located in:



```text

ml/

├── models/

└── scripts/

&#x20;   ├── train.py

&#x20;   ├── predict.py

&#x20;   ├── evaluate.py

&#x20;   └── prepare\_tomato\_dataset.py

```



Trained model files are intentionally excluded from the Git repository through `.gitignore`.



\---



\# ⚙️ Backend



The backend is built using \*\*FastAPI\*\* and provides APIs for:



\* Sensor data

\* Irrigation decisions

\* Crop configuration

\* Agricultural data

\* Plant disease analysis

\* Crop health analysis



\### Main API endpoints



| Method | Endpoint                      | Purpose                   |

| ------ | ----------------------------- | ------------------------- |

| GET    | `/`                           | API status                |

| GET    | `/health`                     | Health check              |

| POST   | `/api/v1/sensor-data`         | Store sensor data         |

| GET    | `/api/v1/sensor-data/latest`  | Get latest sensor data    |

| GET    | `/api/v1/irrigation/status`   | Get irrigation status     |

| POST   | `/api/v1/crops`               | Create crop configuration |

| POST   | `/api/v1/agricultural-data`   | Store agricultural data   |

| GET    | `/api/v1/agricultural-data`   | Get agricultural data     |

| POST   | `/api/v1/plant-image/analyze` | Analyze tomato leaf       |

| POST   | `/api/v1/crop-health/analyze` | Analyze crop health       |

| GET    | `/api/v1/crop-health/live`    | Get live crop health      |



Interactive API documentation is available through FastAPI's Swagger interface at:



```text

/docs

```



\---



\# 🔌 IoT



The planned IoT system uses an \*\*ESP32\*\* connected to agricultural sensors.



Potential sensors/components include:



\* ESP32

\* Soil moisture sensor

\* DHT22 temperature/humidity sensor

\* Soil pH sensor

\* NPK sensor

\* Relay module

\* Water pump

\* Power supply



The ESP32 will communicate sensor readings to the FastAPI backend through Wi-Fi.



IoT code will be maintained under:



```text

iot/

└── esp32/

```



\---



\# 📱 Mobile Application



The mobile application will provide a farmer-friendly interface for the entire system.



Planned screens:



```text

Dashboard

├── Crop Health

├── Soil Moisture

├── Temperature

├── Humidity

└── Irrigation Status



Disease Detection

├── Upload Leaf Image

├── Disease Prediction

├── Confidence

└── Recommendations



Irrigation

├── Pump Status

├── Soil Moisture

└── Irrigation Recommendation



Crop Health

├── pH

├── N

├── P

├── K

├── Temperature

└── Humidity



Weather

├── Current Weather

├── Forecast

└── Weather-based Recommendation



History

└── Sensor \& crop-health data

```



\---



\# 📁 Project Structure



```text

smart-agriculture-ai-iot/

│

├── backend/                  # FastAPI backend

│

├── ml/                       # Machine learning

│   ├── models/               # Trained models (ignored)

│   └── scripts/              # Training/evaluation scripts

│

├── mobile/                   # Mobile application

│

├── iot/                      # ESP32 and sensor code

│

├── docs/                     # Documentation and diagrams

│

├── simulate.py               # Data simulation

│

├── .gitignore

├── README.md

└── LICENSE

```



\---



\# 🛠️ Technology Stack



\### Artificial Intelligence



\* Python

\* PyTorch

\* TorchVision

\* EfficientNet-B0

\* PIL



\### Backend



\* Python

\* FastAPI

\* Uvicorn

\* SQLAlchemy

\* SQLite during development



\### IoT



\* ESP32

\* Temperature \& humidity sensors

\* Soil moisture sensor

\* Soil pH sensor

\* NPK sensing



\### Mobile



\* Mobile application frontend

\* REST API integration



\### Development



\* Git

\* GitHub

\* VS Code



\---



\# 🔐 Privacy \& Security



The system is designed with privacy and security in mind.



\* No unnecessary personal information is collected.

\* Authentication will be implemented for multiple users.

\* Users will only access data associated with their own fields/devices.

\* Secrets and environment variables are excluded from Git.

\* Uploaded files and local databases are excluded from the repository.



\---



\# 👥 Multi-User Architecture



The planned system will support multiple farmers/users.



```text

User

&#x20; ↓

Field

&#x20; ↓

Device

&#x20; ↓

Sensor Data

```



This allows the backend to associate sensor readings, disease analyses, and recommendations with the correct field and user.



\---



\# 🎯 Project Goal



The goal of Smart Agriculture is to provide farmers with a simple platform that answers:



> \*\*"What is happening to my crop, and what should I do?"\*\*



The system combines:



```text

Sensors

&#x20;  +

AI

&#x20;  +

Weather

&#x20;  +

Decision Engine

&#x20;  =

Intelligent Crop Recommendations

```



\---



\# 🚧 Current Development Status



\* \[x] FastAPI backend

\* \[x] Database models

\* \[x] Sensor data API

\* \[x] Irrigation decision API

\* \[x] Crop health analysis

\* \[x] Tomato disease ML model

\* \[x] Plant image analysis API

\* \[x] Recommendation engine

\* \[x] GitHub repository

\* \[ ] ESP32 hardware integration

\* \[ ] Mobile application

\* \[ ] Weather integration

\* \[ ] Multi-user authentication

\* \[ ] Cloud deployment

\* \[ ] End-to-end field testing



\---



\# 📌 Project Status



\*\*Active Development\*\*



This project is being developed as a college AI + IoT project focused on smart and sustainable tomato cultivation.



