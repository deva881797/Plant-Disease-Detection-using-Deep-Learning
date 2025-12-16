"""
Plant Disease Classification Model - Inference Module
Handles model loading, image preprocessing, and predictions.
"""

import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from typing import Tuple, List, Dict, Optional


class PlantDiseaseClassifier:
    """
    A class to handle plant disease classification using EfficientNetB3.
    
    Training Conditions:
        - Architecture: EfficientNetB3 (ImageNet pretrained)
        - Custom layers: BatchNorm -> Dense(256) -> Dropout(0.45) -> Dense(38)
        - Optimizer: Adamax (lr=0.001)
        - Loss: Categorical Crossentropy
        - Preprocessing: Identity function (no normalization, 0-255 range)
        - Data Augmentation: Horizontal flip (training only)
    """
    
    # Class constants matching training configuration
    IMAGE_SIZE = (224, 224)
    CHANNELS = 3
    COLOR_MODE = 'RGB'
    
    def __init__(self, model_path: str, class_dict_path: str):
        """
        Initialize the classifier with model and class dictionary.
        
        Args:
            model_path: Path to the trained .h5 model file
            class_dict_path: Path to the class dictionary CSV file
        """
        self.model_path = model_path
        self.class_dict_path = class_dict_path
        self.model: Optional[keras.Model] = None
        self.class_df: Optional[pd.DataFrame] = None
        self.class_names: Dict[int, str] = {}
        
    def load(self) -> bool:
        """
        Load the model and class dictionary.
        
        Returns:
            True if loading successful, False otherwise
        """
        try:
            self.model = keras.models.load_model(self.model_path)
            self.class_df = pd.read_csv(self.class_dict_path)
            
            # Build class index mapping
            for _, row in self.class_df.iterrows():
                self.class_names[row['class_index']] = row['class']
            
            return True
        except Exception as e:
            print(f"Error loading model or class dictionary: {e}")
            return False
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for model prediction.
        
        During training, the preprocessing_function was an identity function (scalar)
        that returned the image as-is without normalization. The ImageDataGenerator
        kept images in 0-255 range, so we must NOT divide by 255 here.
        
        Args:
            image: PIL Image to preprocess
            
        Returns:
            Preprocessed numpy array ready for prediction
        """
        # Convert to RGB if necessary
        if image.mode != self.COLOR_MODE:
            image = image.convert(self.COLOR_MODE)
        
        # Resize image to match training size (224x224)
        image = image.resize(self.IMAGE_SIZE)
        
        # Convert to numpy array - keep as float32 but DON'T normalize
        # Training used: preprocessing_function=scalar where scalar(img) returns img as-is
        img_array = np.array(image, dtype=np.float32)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image: Image.Image) -> np.ndarray:
        """
        Get prediction probabilities for an image.
        
        Args:
            image: PIL Image to classify
            
        Returns:
            Array of prediction probabilities for each class
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image, verbose=0)
        return predictions[0]
    
    def classify(self, image: Image.Image, top_k: int = 5) -> List[Dict]:
        """
        Classify an image and return top-k predictions.
        
        Args:
            image: PIL Image to classify
            top_k: Number of top predictions to return
            
        Returns:
            List of dictionaries with class info and confidence
        """
        predictions = self.predict(image)
        
        # Get top-k indices
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            class_name = self.class_names.get(idx, "Unknown")
            plant_name, condition = self.format_class_name(class_name)
            is_healthy = self.is_healthy(class_name)
            
            results.append({
                'class_index': int(idx),
                'class_name': class_name,
                'plant_name': plant_name,
                'condition': condition,
                'is_healthy': is_healthy,
                'confidence': float(predictions[idx]),
                'confidence_percent': float(predictions[idx] * 100)
            })
        
        return results
    
    @staticmethod
    def format_class_name(class_name: str) -> Tuple[str, str]:
        """
        Format class name for display.
        
        Args:
            class_name: Raw class name from dataset
            
        Returns:
            Tuple of (plant_name, condition)
        """
        parts = class_name.split('___')
        plant = parts[0].replace('_', ' ')
        condition = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
        return plant, condition
    
    @staticmethod
    def is_healthy(class_name: str) -> bool:
        """
        Determine if the class represents a healthy plant.
        
        Args:
            class_name: Class name to check
            
        Returns:
            True if plant is healthy, False otherwise
        """
        return 'healthy' in class_name.lower()
    
    def get_num_classes(self) -> int:
        """Get the number of classes the model can predict."""
        return len(self.class_names)
    
    def get_all_classes(self) -> List[str]:
        """Get list of all class names."""
        return list(self.class_names.values())
    
    def get_training_info(self) -> Dict:
        """
        Get information about the model's training configuration.
        
        Returns:
            Dictionary with training details
        """
        return {
            'architecture': 'EfficientNetB3',
            'pretrained_weights': 'ImageNet',
            'input_size': f'{self.IMAGE_SIZE[0]} × {self.IMAGE_SIZE[1]} × {self.CHANNELS}',
            'color_mode': self.COLOR_MODE,
            'num_classes': self.get_num_classes(),
            'optimizer': 'Adamax',
            'learning_rate': 0.001,
            'loss_function': 'Categorical Crossentropy',
            'custom_layers': [
                'BatchNormalization (axis=-1, momentum=0.99, epsilon=0.001)',
                'Dense(256, activation=relu, L2=0.016, L1_activity=0.006, L1_bias=0.006)',
                'Dropout(rate=0.45, seed=123)',
                'Dense(38, activation=softmax)'
            ],
            'data_augmentation': {
                'training': ['Horizontal Flip'],
                'validation': [],
                'test': []
            },
            'preprocessing': 'Identity (no normalization, 0-255 range)'
        }
