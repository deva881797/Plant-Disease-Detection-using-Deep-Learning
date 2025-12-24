"""Plant Disease Classification - REST API"""

import logging
import sys
from io import BytesIO
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

from model import PlantDiseaseClassifier

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

# Constants
MODEL_PATH = "prediction_model.tflite"
CLASS_DICT_PATH = "Plant Village Disease-class_dict.csv"

# Initialize FastAPI app
app = FastAPI(
    title="Plant Disease Classification API",
    description="AI-powered plant disease detection from leaf images",
    version="1.0.0",
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load classifier at startup
classifier = None


class Prediction(BaseModel):
    """Single prediction result."""

    plant: str
    disease: str
    confidence: float
    is_healthy: bool


class PredictionResponse(BaseModel):
    """API response for predictions."""

    success: bool
    predictions: List[Prediction]


class HealthResponse(BaseModel):
    """API health check response."""

    status: str
    model_loaded: bool


class ClassesResponse(BaseModel):
    """API response for available classes."""

    total_classes: int
    classes: List[str]


class ErrorResponse(BaseModel):
    """API error response."""

    success: bool
    error: str


@app.on_event("startup")
async def load_model():
    """Load the classifier model on startup."""
    global classifier
    try:
        classifier = PlantDiseaseClassifier(MODEL_PATH, CLASS_DICT_PATH)
        if not classifier.load():
            logging.error("Failed to load classifier model")
            classifier = None
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        classifier = None


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", model_loaded=classifier is not None)


@app.get("/api/classes", response_model=ClassesResponse)
async def get_classes():
    """Get all available disease classes."""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    classes = classifier.get_all_classes()
    return ClassesResponse(total_classes=len(classes), classes=classes)


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Predict plant disease from an uploaded image.

    - **file**: Image file (JPEG, PNG, etc.)

    Returns top-5 predictions with confidence scores.
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Get predictions
        results = classifier.classify(image, top_k=5)

        # Format response
        predictions = [
            Prediction(
                plant=r["plant_name"],
                disease=r["condition"],
                confidence=round(r["confidence_percent"], 2),
                is_healthy=r["is_healthy"],
            )
            for r in results
        ]

        return PredictionResponse(success=True, predictions=predictions)

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image")


# For running locally: uvicorn api:app --host 0.0.0.0 --port 8000
