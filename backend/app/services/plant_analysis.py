from pathlib import Path
import shutil

import torch
from torch import nn
from torchvision import transforms, models
from PIL import Image

from app.services.recommendation_engine import generate_recommendation


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "backend" / "uploads" / "plants"

MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "models"
    / "tomato_efficientnet_b0_best.pth"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# IMAGE TRANSFORMATION
# ============================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# LOAD TOMATO DISEASE MODEL
# ============================================================

print("Loading tomato disease model...")

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Tomato disease model not found at: {MODEL_PATH}"
    )


checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

CLASS_NAMES = checkpoint["class_names"]


model = models.efficientnet_b0(
    weights=None
)

num_features = model.classifier[1].in_features

model.classifier[1] = nn.Linear(
    num_features,
    len(CLASS_NAMES)
)


model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(DEVICE)

model.eval()


print("Tomato disease model loaded successfully.")
print(f"Model device: {DEVICE}")

if torch.cuda.is_available():

    print(
        f"GPU: {torch.cuda.get_device_name(0)}"
    )


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path: Path):

    """
    Run the trained tomato disease model
    on a single image.
    """

    image = Image.open(
        image_path
    ).convert("RGB")


    input_tensor = transform(
        image
    )

    input_tensor = input_tensor.unsqueeze(0)

    input_tensor = input_tensor.to(
        DEVICE
    )


    with torch.no_grad():

        outputs = model(
            input_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_index = torch.max(
            probabilities,
            dim=1
        )


    predicted_class = CLASS_NAMES[
        predicted_index.item()
    ]


    confidence_percentage = (
        confidence.item() * 100
    )


    # ========================================================
    # TOP 3 PREDICTIONS
    # ========================================================

    top_probabilities, top_indices = torch.topk(
        probabilities[0],
        min(3, len(CLASS_NAMES))
    )


    top_predictions = []


    for probability, index in zip(
        top_probabilities,
        top_indices
    ):

        top_predictions.append({

            "disease": CLASS_NAMES[
                index.item()
            ],

            "confidence": round(
                probability.item() * 100,
                2
            )
        })


    return {

        "disease": predicted_class,

        "confidence": round(
            confidence_percentage,
            2
        ),

        "top_predictions": top_predictions
    }


# ============================================================
# ANALYZE UPLOADED PLANT IMAGE
# ============================================================

def analyze_plant_image(
    filename: str,
    file,
    soil_moisture=None,
    temperature=None,
    humidity=None,
    soil_ph=None,
    nitrogen=None,
    phosphorus=None,
    potassium=None
):

    """
    Save the uploaded tomato plant image,
    run the AI disease model,
    and generate an agricultural recommendation.
    """

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    safe_filename = Path(
        filename
    ).name


    file_path = (
        UPLOAD_DIR
        / safe_filename
    )


    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file,
            buffer
        )


    # --------------------------------------------------------
    # AI DISEASE PREDICTION
    # --------------------------------------------------------

    prediction = predict_disease(
        file_path
    )


    # --------------------------------------------------------
    # AGRICULTURAL RECOMMENDATION
    # --------------------------------------------------------

    recommendation = generate_recommendation(

        disease=prediction["disease"],

        confidence=prediction["confidence"],

        soil_moisture=soil_moisture,

        temperature=temperature,

        humidity=humidity,

        soil_ph=soil_ph,

        nitrogen=nitrogen,

        phosphorus=phosphorus,

        potassium=potassium
    )


    # --------------------------------------------------------
    # FINAL API RESPONSE
    # --------------------------------------------------------

    return {

        "filename": safe_filename,

        "saved_path": str(
            file_path
        ),

        "status": "analysis_complete",

        "prediction": prediction,

        "recommendation": recommendation
    }