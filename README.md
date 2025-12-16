# 🌿 Plant Village Disease Classifier

A deep learning web application for identifying plant diseases from leaf images using DenseNet121 architecture.

![Model Accuracy](https://img.shields.io/badge/Accuracy-98.55%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)

## 📋 Overview

This application uses a trained DenseNet121 model to classify 38 different plant conditions (healthy and diseased) across 14 plant species from the Plant Village dataset.

### Supported Plants
- 🍎 Apple | 🫐 Blueberry | 🍒 Cherry | 🌽 Corn
- 🍇 Grape | 🍊 Orange | 🍑 Peach | 🫑 Pepper
- 🥔 Potato | 🫐 Raspberry | 🫘 Soybean | 🎃 Squash
- 🍓 Strawberry | 🍅 Tomato

## ⚙️ Training Conditions

The model was trained under the following specific conditions:

### Model Architecture

```
DenseNet121 (ImageNet pretrained, include_top=False, pooling='max')
└── BatchNormalization (axis=-1, momentum=0.99, epsilon=0.001)
    └── Dense(256, activation='relu')
        ├── L2 kernel regularization: 0.016
        ├── L1 activity regularization: 0.006
        └── L1 bias regularization: 0.006
    └── Dropout(rate=0.45, seed=123)
        └── Dense(38, activation='softmax')
```

### Training Parameters

| Parameter | Value |
|-----------|-------|
| **Optimizer** | Adamax |
| **Learning Rate** | 0.001 |
| **Loss Function** | Categorical Crossentropy |
| **Input Size** | 224 × 224 × 3 (RGB) |

### Data Augmentation

**Training Data:**
- Horizontal Flip: Enabled
- Shuffle: Enabled

**Validation/Test Data:**
- No augmentation
- Test Shuffle: Disabled

### Library Versions (from `version.txt`)

| Library | Version |
|---------|---------|
| Python | 3.7.12 |
| NumPy | 1.21.6 |
| Pandas | 1.3.5 |
| Matplotlib | 3.5.3 |
| Scikit-learn | 1.0.2 |
| Seaborn | 0.12.2 |
| OpenCV | 4.5.4 |
| Pillow | 9.3.0 |
| TensorFlow | 2.11.0 |
| Keras | 2.11.0 |

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually:**
   ```bash
   docker build -t plant-disease-classifier .
   docker run -p 8501:8501 plant-disease-classifier
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

### Local Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
Plant Village/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker configuration
├── docker-compose.yml                  # Docker Compose configuration
├── .dockerignore                       # Docker ignore rules
├── .streamlit/
│   └── config.toml                     # Streamlit configuration
├── densenet121-Plant Village Disease-98.55.h5  # Trained model
├── Plant Village Disease-class_dict.csv          # Class labels
├── version.txt                         # Training environment versions
└── README.md                           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Server port | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Server address | 0.0.0.0 |

### Resource Requirements

- **Minimum RAM:** 2GB
- **Recommended RAM:** 4GB
- **Disk Space:** ~500MB (including model)

## 📊 Model Performance

- **Architecture:** DenseNet121
- **Accuracy:** 98.55%
- **Input Size:** 224 × 224 pixels
- **Number of Classes:** 38

## 📝 Usage Tips

1. **Image Quality:** Use clear, well-lit images for best results
2. **Focus:** Center the leaf in the image
3. **Affected Area:** Capture any visible symptoms clearly
4. **Multiple Predictions:** Check the top 5 predictions for ambiguous cases

## 🐳 Docker Commands

```bash
# Build the image
docker build -t plant-disease-classifier .

# Run the container
docker run -p 8501:8501 plant-disease-classifier

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## 📜 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Plant Village Dataset
- DenseNet Architecture
- Streamlit Framework
