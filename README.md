# 🌿 Plant Village Disease Classifier

A high-performance deep learning web application for identifying plant diseases from leaf images using **DenseNet121 architecture** with **TensorFlow Lite** optimization.

![Model Accuracy](https://img.shields.io/badge/Accuracy-98.55%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Model Format](https://img.shields.io/badge/Model-TFLite-yellow)

## 📋 Overview

This application uses a trained **DenseNet121** model (converted to **TensorFlow Lite** for optimal performance) to classify **38 different plant conditions** (healthy and diseased) across **14 plant species** from the Plant Village dataset.

### ✨ Key Features

- 🚀 **Ultra-Fast Inference:** 5x faster predictions using TensorFlow Lite
- 💾 **Optimized Model Size:** 42.3 MB (67% smaller than original H5 format)
- 🎯 **High Accuracy:** 98.55% classification accuracy maintained
- 🐳 **Docker Ready:** Complete containerization with live reload for development  
- 💻 **Low Resource Usage:** Perfect for deployment on limited resources (0.5GB RAM)
- 🎨 **Modern UI:** Premium Streamlit interface with real-time predictions
- 📊 **Top-K Predictions:** View confidence scores for top 5 predictions
- 💊 **Prevention & Treatment:** Get medication and prevention tips for detected diseases

### Supported Plants

- 🍎 Apple | 🫐 Blueberry | 🍒 Cherry | 🌽 Corn
- 🍇 Grape | 🍊 Orange | 🍑 Peach | 🫑 Pepper
- 🥔 Potato | 🫐 Raspberry | 🫘 Soybean | 🎃 Squash
- 🍓 Strawberry | 🍅 Tomato

## 🏗️ Model Architecture

### DenseNet121 (TensorFlow Lite Optimized)

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
| **Preprocessing** | No normalization (0-255 range) |

### Data Augmentation

**Training Data:**
- Horizontal Flip: Enabled
- Shuffle: Enabled

**Validation/Test Data:**
- No augmentation
- Test Shuffle: Disabled

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Start the application:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

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
├── app.py                                   # Main Streamlit application
├── model.py                                 # TFLite model wrapper & inference
├── ui.py                                    # UI components & styling
├── requirements.txt                         # Python dependencies
├── Dockerfile                               # Docker configuration
├── docker-compose.yml                       # Docker Compose setup
├── .dockerignore                            # Docker ignore rules
├── .streamlit/
│   └── config.toml                          # Streamlit configuration
├── prediction_model.tflite                  # Optimized TFLite model (42.3 MB)
├── Plant Village Disease-class_dict.csv    # Class labels mapping
└── README.md                                # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Server port | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Server address | 0.0.0.0 |
| `STREAMLIT_SERVER_HEADLESS` | Headless mode | true |
| `STREAMLIT_SERVER_RUN_ON_SAVE` | Live reload | true |

### Resource Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **RAM** | 512 MB | 2 GB |
| **CPU** | 0.1 vCPU | 1 vCPU |
| **Disk Space** | 200 MB | 500 MB |
| **Docker** | 20.10+ | Latest |

## 📊 Model Performance

### Metrics

- **Architecture:** DenseNet121 (TFLite)
- **Accuracy:** 98.55%
- **Model Size:** 42.3 MB
- **Format:** TensorFlow Lite (.tflite)
- **Input Size:** 224 × 224 pixels
- **Number of Classes:** 38

### Performance Comparison

| Metric | H5 Format | TFLite Format | Improvement |
|--------|-----------|---------------|-------------|
| **Model Size** | 128.8 MB | 42.3 MB | **67% smaller** |
| **Inference Speed** | 221 ms | ~43 ms | **5.1x faster** |
| **Memory Usage** | High | Low | **Optimized** |
| **Accuracy** | 98.55% | 98.55% | **Maintained** |

## 📝 Usage Tips

1. **Image Quality:** Use clear, well-lit images for best results
2. **Focus:** Center the affected leaf area in the image
3. **Lighting:** Avoid shadows and overexposure
4. **File Format:** Supports JPG, JPEG, PNG
5. **Multiple Predictions:** Review top 5 predictions for confidence scores

## 🐳 Docker Commands

```bash
# Start the application
docker-compose up -d

# Rebuild and start (after code changes)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Restart the container
docker-compose restart

# Stop and remove containers
docker-compose down

# Check container status
docker ps
```

## 🔧 Development

### Live Reload

The Docker setup includes volume mounts for live reload:
- `app.py` - Main application
- `model.py` - Model logic
- `ui.py` - UI components

Changes to these files are automatically reflected without rebuilding.

### Testing

```bash
# Run inside the container
docker exec plant-village-dev python -c "from model import PlantDiseaseClassifier; print('Model loads OK')"
```

## 🚢 Deployment

Perfect for deployment on:
- ☁️ Render (Free Tier: 0.5GB RAM, 0.1 CPU)
- 🌊 Railway
- 🔷 Heroku
- ☁️ Google Cloud Run
- 📦 AWS Elastic Beanstalk

## 🎯 Why TensorFlow Lite?

- **Faster Inference:** 5x faster predictions vs standard TensorFlow
- **Smaller Size:** 67% reduction in model file size
- **Lower Memory:** Optimized for resource-constrained environments
- **Production Ready:** Industry standard for deployment
- **No Accuracy Loss:** Maintains full 98.55% accuracy

## 📜 License

This project is for educational purposes.

## 🙏 Acknowledgments

- **Plant Village Dataset** - Training data source
- **DenseNet Architecture** - Base model architecture
- **TensorFlow Lite** - Model optimization framework
- **Streamlit** - Web application framework

---

**Made with ❤️ for plant disease detection**
