"""Plant Disease Classification using CNN - Main Application

This version uses FastAPI as the model server to reduce RAM usage.
Streamlit acts as a lightweight UI that calls the API for predictions.
"""

import logging
import os
import sys
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

from ui import PlantDiseaseUI

# Configure logging - logs go to server, not exposed to users
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

# API Configuration - Internal call to FastAPI (bypasses nginx)
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
API_SECRET_KEY = os.environ.get("API_SECRET_KEY", "")

# Static training info (no need to load model for this)
TRAINING_INFO = {
    "architecture": "DenseNet121 (TFLite)",
    "pretrained_weights": "ImageNet",
    "input_size": "224 × 224 × 3",
    "color_mode": "RGB",
    "num_classes": 38,
    "optimizer": "Adamax",
    "learning_rate": 0.001,
    "loss_function": "Categorical Crossentropy",
    "model_format": "TensorFlow Lite",
    "model_size": "42.3 MB",
    "performance": "5x faster inference vs H5",
    "custom_layers": [
        "BatchNormalization (axis=-1, momentum=0.99, epsilon=0.001)",
        "Dense(256, activation=relu, L2=0.016, L1_activity=0.006, L1_bias=0.006)",
        "Dropout(rate=0.45, seed=123)",
        "Dense(38, activation=softmax)",
    ],
    "data_augmentation": {
        "training": ["Horizontal Flip"],
        "validation": [],
        "test": [],
    },
    "preprocessing": "Identity (no normalization, 0-255 range)",
}


def check_api_health() -> bool:
    """Check if the FastAPI backend is available."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("model_loaded", False)
        return False
    except requests.RequestException:
        return False


def classify_image(image: Image.Image, top_k: int = 5) -> list | None:
    """
    Send image to FastAPI for classification.

    Args:
        image: PIL Image to classify
        top_k: Number of top predictions to return

    Returns:
        List of prediction dictionaries matching the classifier.classify() format
    """
    try:
        # Convert PIL Image to bytes
        img_buffer = BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Prepare headers with API key if configured
        headers = {}
        if API_SECRET_KEY:
            headers["X-API-Key"] = API_SECRET_KEY

        # Send to FastAPI
        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            files={"file": ("image.png", img_buffer, "image/png")},
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                # Convert API response to classifier.classify() format
                predictions = []
                for pred in data.get("predictions", [])[:top_k]:
                    # Reconstruct class_name from plant and disease
                    plant_name = pred.get("plant", "Unknown")
                    condition = pred.get("disease", "Unknown")
                    class_name = f"{plant_name.replace(' ', '_')}___{condition.replace(' ', '_')}"

                    predictions.append(
                        {
                            "class_index": 0,  # Not available from API
                            "class_name": class_name,
                            "plant_name": plant_name,
                            "condition": condition,
                            "is_healthy": pred.get("is_healthy", False),
                            "confidence": pred.get("confidence", 0)
                            / 100,  # Convert back to 0-1
                            "confidence_percent": pred.get("confidence", 0),
                        }
                    )
                return predictions

        # Handle non-200 responses
        logging.error(f"API returned status {response.status_code}")
        return None

    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None


def _handle_image_prediction(ui: PlantDiseaseUI, image: Image.Image) -> list | None:
    """Handle image upload and prediction, returning predictions if successful."""
    try:
        with st.spinner("🔄 Analyzing image..."):
            predictions = classify_image(image, top_k=5)
            if predictions:
                ui.render_results(predictions)
                return predictions
            else:
                st.error("⚠️ Unable to process image. Please try again. (Error 500)")
                if st.button("🔄 Try Again", key="retry_predict"):
                    st.rerun()
                return None
    except Exception as e:
        logging.error(f"Classification failed: {e}")
        st.error("⚠️ Unable to process image. Please try again. (Error 500)")
        if st.button("🔄 Try Again", key="retry_exception"):
            st.rerun()
        return None


def main():
    """Main app entry point."""
    try:
        # Initialize UI
        ui = PlantDiseaseUI()

        # Check API health
        if not check_api_health():
            ui.render_error(
                "⚠️ Service temporarily unavailable. Please try again later. (Error 503)"
            )
            if st.button("🔄 Retry", key="retry_health"):
                st.rerun()
            st.stop()

        # Render sidebar with static training info
        ui.render_sidebar(TRAINING_INFO)

        # Render main header
        ui.render_header()

        # Create two columns for layout
        col1, col2 = st.columns([1, 1], gap="large")

        # Handle image upload and prediction
        predictions = None
        with col1:
            image = ui.render_upload_section()

        with col2:
            if image is not None:
                predictions = _handle_image_prediction(ui, image)
            else:
                ui.render_placeholder()

        # Show prevention and medication for detected disease
        if predictions:
            ui.render_prevention_and_medication(predictions[0])

        # Footer
        ui.render_footer()

    except Exception as e:
        logging.error(f"Unhandled application error: {e}")
        st.error("⚠️ An unexpected error occurred. Please try again later. (Error 500)")
        if st.button("🔄 Reload Page", key="retry_unhandled"):
            st.rerun()


if __name__ == "__main__":
    main()
