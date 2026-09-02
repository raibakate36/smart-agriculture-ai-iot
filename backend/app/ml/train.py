import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATA_PATH = "../../data/processed/agricultural_training.csv"

df = pd.read_csv(DATA_PATH)


# --------------------------------------------------
# 2. Define features and target
# --------------------------------------------------

FEATURES = [
    "soil_ph",
    "nitrogen",
    "phosphorus",
    "potassium",
    "soil_moisture",
    "temperature",
    "humidity"
]

TARGET = "target"


X = df[FEATURES]
y = df[TARGET]


# --------------------------------------------------
# 3. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 4. Create model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------------------------
# 5. Train
# --------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------
# 6. Evaluate
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# --------------------------------------------------
# 7. Save model
# --------------------------------------------------

MODEL_PATH = "../../data/models/agricultural_model.pkl"

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")