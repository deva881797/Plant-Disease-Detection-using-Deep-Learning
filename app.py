"""Plant Disease Classification using CNN - Main Application"""

import logging
import sys

import streamlit as st

from model import PlantDiseaseClassifier
from ui import PlantDiseaseUI

# Configure logging - logs go to server, not exposed to users
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

# Constants - File paths
MODEL_PATH = "prediction_model.tflite"
CLASS_DICT_PATH = "Plant Village Disease-class_dict.csv"


@st.cache_resource
def get_classifier() -> PlantDiseaseClassifier:
    """Load and cache the classifier model."""
    classifier = PlantDiseaseClassifier(MODEL_PATH, CLASS_DICT_PATH)
    if not classifier.load():
        raise RuntimeError("Failed to load classifier model")
    return classifier


def main():
    """Main app entry point."""
    try:
        # Initialize UI
        ui = PlantDiseaseUI()

        # Load classifier
        try:
            classifier = get_classifier()
        except RuntimeError as e:
            logging.error(f"Model loading failed: {e}")
            ui.render_error(
                "⚠️ Service temporarily unavailable. Please try again later. (Error 503)"
            )
            st.stop()

        # Get training info and version
        training_info = classifier.get_training_info()

        # Render sidebar
        ui.render_sidebar(training_info)

        # Render main header
        ui.render_header()

        # Create two columns for layout
        col1, col2 = st.columns([1, 1], gap="large")

        # Store predictions for use outside columns
        predictions = None

        with col1:
            # Image upload section
            image = ui.render_upload_section()

        with col2:
            if image is not None:
                # Classify and show results
                try:
                    with st.spinner("🔄 Analyzing image..."):
                        predictions = classifier.classify(image, top_k=5)
                        ui.render_results(predictions)
                except Exception as e:
                    logging.error(f"Classification failed: {e}")
                    st.error("⚠️ Unable to process image. Please try again. (Error 500)")
            else:
                # Show placeholder
                ui.render_placeholder()

        # Prevention and medication section - show only for the detected disease
        if predictions:
            ui.render_prevention_and_medication(predictions[0])

        # Footer
        ui.render_footer()

    except Exception as e:
        # Catch-all for any unhandled exceptions
        logging.error(f"Unhandled application error: {e}")
        st.error(
            "⚠️ An unexpected error occurred. Our team has been notified. Please try again later. (Error 500)"
        )


if __name__ == "__main__":
    main()
