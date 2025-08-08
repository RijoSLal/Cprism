# 🧠 Product Detection - One Shot Simulated Object Detection

This project implements a **one-shot simulated object detection service, detect product from supermarket shelves**, where a limited number of individual product images are used to generate large-scale, high-quality annotated datasets by matching these products against various background images. 

Using this simulation strategy, you can **rapidly scale your dataset** for object detection tasks even with only a few real product images making it ideal for low-data environments or rapid prototyping.

---

## 🔍 Key Features

* **One-Shot Simulation**: Automatically generates annotated detection datasets from limited product images.
* **YOLOv8n Object Detection Model**: Lightweight and fast model architecture used for product detection.
* **MLflow Integration**: The detection model is stored and versioned on MLflow via DagsHub.
* **Hosted Fastapi Service**: The object detection model is exposed through API.
* **Minimal Data Requirement**: Proven with just 2 products in the sample dataset.

---

## 🌍 Hosted API

📡 **Public Endpoint**:
[http://ec2-51-21-252-101.eu-north-1.compute.amazonaws.com:8000/](http://ec2-51-21-252-101.eu-north-1.compute.amazonaws.com:8000/)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RijoSLal/Cprism.git
cd Cprism/service
```

### 2. Configure Environment

Create a `.env` file in the `service` directory:

```env
MODEL_NAME="<your-model-name>"
VERSION="<model-version>"
URI="https://dagshub.com/slalrijo2005/Cprism.mlflow"
```

> This tells the API server which model version to fetch from MLflow at runtime.

---

### 3. Build & Run the API Service with Docker

```bash
docker build -t product-detection-service .
docker run --env-file .env -p 8000:8000 product-detection-service
```

The service will automatically pull the **YOLOv8n model** from the MLflow registry hosted at:

🔗 [https://dagshub.com/slalrijo2005/Cprism.mlflow](https://dagshub.com/slalrijo2005/Cprism.mlflow)

---

## 🧪 Synthetic Data Generation

To generate simulated object detection datasets:

📁 **Notebook**:

```bash
experiment/experiment.ipynb
```

This notebook:

* Paste product cutouts to background scenes
* Automatically generates realistic synthetic images
* Outputs YOLO-format annotations for training

Perfect for expanding small datasets into rich training corpora.

---

## 🤝 How to Integrate the API in Your App

📄 **File**:

```bash
experiment/How_to_use.py
```

This script demonstrates how to:

* Connect to the running object detection API
* Send image files for inference
* Receive results

Use this as a base for integrating the detection service into any external application (e.g., mobile apps, retail systems, automation workflows).

---

## 📦 Sample Products

This experiment currently uses **2 product categories**, located in:

📁 [`experiment/examples/classes`]


---
