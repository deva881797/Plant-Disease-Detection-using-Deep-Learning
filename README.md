# 🌿 Plant Village Disease Classifier

A high-performance deep learning web application for identifying plant diseases from leaf images using **DenseNet121 architecture** with **TensorFlow Lite** optimization.

![Model Accuracy](https://img.shields.io/badge/Accuracy-98.55%25-success)
![Python](https://img.shields.io/badge/Python-3.10-3776AB)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-FF6F00)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52.2-FF4B4B)
![Model Format](https://img.shields.io/badge/Model-DenseNet121_TFLite-8E44AD)
![Deployment](https://img.shields.io/badge/Hosting-Render-2C2FF3)

---

## 📋 Overview

The **Plant Village Disease Classifier** is a production-ready deep learning application designed to identify plant diseases from leaf images with high accuracy and low resource usage. The system is optimized for real-world deployment and runs efficiently even on low-tier cloud infrastructure like Render's Free tier.

The solution is built using a **DenseNet121-based model optimized with TensorFlow Lite**, exposed through a secure REST API and consumed by a lightweight web interface.

---

## 🚀 Live Demo

**Try it now:** [plant-disease-detection-using-deep-c44z.onrender.com](https://plant-disease-detection-using-deep-c44z.onrender.com/)

---

## ✨ Key Highlights

*   🎯 **High Accuracy**: Achieves **98.55% accuracy** on the Plant Village dataset (14 species, 38 conditions).
*   ⚡ **Inference Speed**: Optimized with **TensorFlow Lite**, reducing latency to **~43ms** (5x faster than standard H5).
*   💾 **Memory Efficiency**: Reduced RAM usage by **63% (~366 MiB)** through a custom shared model architecture.
*   🔒 **Enterprise Security**: Secured with mandatory API key authentication and sanitized error handling.
*   🐳 **Cloud Ready**: Fully containerized with Nginx reverse proxy, ready for 0.5GB RAM environments.

---

## 🏗️ System Architecture

The application follows a **"Single Model Owner"** design pattern. The heavy TFLite model is loaded only by the FastAPI service, while the Streamlit UI acts as a thin client. This prevents duplicate memory overhead and improves system resilience.

```
graph LR
    User["👤 User Browser"] --> Nginx

    subgraph Docker["🐳 Docker Container (:8501)"]
        Nginx["🌐 Nginx<br/>Reverse Proxy"]
        Streamlit["🖥️ Streamlit UI<br/>(Lightweight Client)"]
        FastAPI["⚙️ FastAPI Service<br/>(Model Owner)"]
        Model["🧠 TFLite Model<br/>(42.3 MB)"]

        Nginx --> Streamlit
        Streamlit -- "Internal API Call" --> FastAPI
        FastAPI --> Model
        Nginx -. "/api/* (External)" .-> FastAPI
    end
```

**Design Philosophy**: Keep the UI thin, the API stateless, and the model centralized for maximum efficiency and scalability.

---

## 🔄 Functional Flow

1.  **Access**: The user interacts with the Streamlit interface via Nginx.
2.  **Routing**: Nginx handles internal routing between the UI and the Backend API.
3.  **Inference**: When an image is uploaded, the UI sends a request to FastAPI.
4.  **Processing**: FastAPI processes the image using the centralized TFLite model.
5.  **Insight**: Results are returned with confidence scores and actionable prevention/medication tips.

---

## 🔌 REST API

The backend exposes a secured REST API that can be consumed by external systems such as mobile apps.

### Available Endpoints
*   `GET  /api/health` – Service and model health check.
*   `POST /api/predict` – Upload an image and receive top-5 predictions (Secured).
*   `GET  /api/classes` – Retrieve all 38 supported disease classes (Secured).

### Security Measures
*   **API Key Authentication**: Mandatory `X-API-Key` header for predictive endpoints.
*   **Input Validation**: Strict image-type filtering and size checks.
*   **Secure Headers**: CORS restricted and internal stack traces sanitized.

---

## 📊 Performance Benchmark

| Metric | Original (H5) | **Optimized (TFLite)** | Improvement |
|--------|---------------|-----------------------|-------------|
| **Model Size** | 128.8 MB | **42.3 MB** | **67% Smaller** |
| **Inference Time** | 221 ms | **43.3 ms** | **5.1x Faster** |
| **RAM (Total)**| ~1.1 GB | **~366 MiB** | **63% Saved** |
| **Accuracy** | 98.55% | **98.55%** | **Maintained** |

---

## 🚀 Deployment

### Docker (Recommended)
The entire system is containerized for consistent deployment across environments.
```bash
docker-compose up -d --build
```
*   **UI**: `http://localhost:8501`
*   **API**: `http://localhost:8501/api/health`

### Local Development
```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
streamlit run app.py
```

---

## 📁 Project Structure

```text
├── app.py                  # Streamlit UI (Thin Client)
├── api.py                  # FastAPI Backend (Model Owner)
├── model.py                # TFLite Inference Logic
├── ui.py                   # UI Modules & Premium Styling
├── nginx.conf              # Reverse Proxy Configuration
├── start.sh                # Container Multi-service Entrypoint
├── prediction_model.tflite # Optimized Weights
└── requirements.txt        # Pinned Dependencies
```

---

## 🎯 Conclusion

This project demonstrates expertise in **machine learning engineering, backend optimization, and DevOps**. By refactoring the architecture to share a single model instance and optimizing the weights with TFLite, we achieved a production-ready system that is both lightning-fast and extremely cost-effective to host.

---

**Built with a focus on performance, security, and production readiness.**
