# 🔐 Phishing URL Detection API

This project provides a machine learning-based API to detect whether a given URL is **phishing** or **legitimate**. It is built using **FastAPI** and deployed on **Render** for easy public access.

## 🚀 Features

- 🔍 Detects phishing URLs using a trained ML model.
- 🌐 Deployed API with interactive Swagger UI at `/docs`.
- ⚡ Fast and scalable with FastAPI.
- 🔧 Easy to run locally or deploy in the cloud.

---

## 🛠 Tech Stack

- **FastAPI** – Web framework for building APIs.
- **Uvicorn** – ASGI server for local development.
- **Gunicorn** – Production server for deployment.
- **Scikit-learn** – Machine Learning model training and inference.
- **Pandas**, **NumPy** – Data processing and numerical operations.
- **tldextract** – Extracts domain information from URLs.

---
Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
---

Start the ASGI server locally on port 8000:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



