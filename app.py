"""Plant Disease Classifier - Main Application"""

import streamlit as st

from model import PlantDiseaseClassifier
from ui import PlantDiseaseUI

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

    # Initialize UI
    ui = PlantDiseaseUI()

    # Load classifier
    try:
        classifier = get_classifier()
    except RuntimeError as e:
        ui.render_error(f"Failed to load model: {e}")
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
            with st.spinner("🔄 Analyzing image..."):
                predictions = classifier.classify(image, top_k=5)
                ui.render_results(predictions)
        else:
            # Show placeholder
            ui.render_placeholder()

    # Prevention and medication section - show only for the detected disease
    if predictions:
        ui.render_prevention_and_medication(predictions[0])

    # Footer
    ui.render_footer()


if __name__ == "__main__":
    main()
