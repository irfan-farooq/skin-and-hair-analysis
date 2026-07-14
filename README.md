<div align="center">

# 🧴 SkinMax

### AI-powered skin & hair analysis with custom-trained ML models, personalized routines, progress tracking, and real-time environmental guidance

## 📌 What is SkinMax?

SkinMax is a personalized skin and hair analysis web application that uses computer vision and machine learning to analyze a user's facial features and deliver tailored skincare routines, lifestyle advice, color recommendations, and dynamically updated environmental skincare guidance — all without relying on any external AI API.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔬 **Skin & Color Analysis** | Skin tone, undertone, eye color, and lip color detection via pure CV mathematics in HSV and LAB colorspaces |
| 🧠 **Custom-Trained ML Models** | Three models trained from scratch — acne detection, hair texture, and face shape classification |
| 📋 **Personalized Routines** | Modular template engine assembles morning/night routines and lifestyle tips from combined analysis output |
| 💬 **Contextual Chatbot** | TF-IDF chatbot with personal analysis loaded as context for follow-up skincare questions |
| 📈 **Progress Tracking** | Weighted skin health scoring across multiple scans with trend visualization |
| 👯 **Skin Twin Matching** | Cosine similarity matching to connect users with similar skin profiles |
| 🌍 **Environmental Guidance** | Real-time UV, humidity, and pollution-aware recommendations via OpenWeatherMap API |
| 🔔 **Smart Reminders** | AM/PM push notifications for skincare routines via APScheduler + Firebase Cloud Messaging |
| 🤝 **Community Routines** | Real-time routine sharing via Go WebSockets |

---

## 🧠 ML Pipeline

The core of SkinMax is a multi-stage ML pipeline built entirely in Python. Every model returns a **confidence score** alongside its prediction.

### Computer Vision (No Model Required)
Using **MediaPipe** for facial landmark detection and **OpenCV** for pixel-level analysis:
- **Skin tone & undertone** — LAB colorspace analysis on cheek and forehead regions
- **Eye color** — Iris segmentation using MediaPipe refined landmarks (indices 469–477), pupil exclusion masking, and HSV/LAB median classification
- **Lip color** — OpenCV contour analysis on MediaPipe lip landmarks

### Custom-Trained Models

#### 1. Acne Detection — YOLOv8-nano
- **Architecture:** YOLOv8-nano (Ultralytics)
- **Dataset:** ACNE04 (fine-tuned from pretrained weights)
- **Task:** Acne severity grading and zone detection (forehead, cheeks, chin, nose)
- **Output:** Bounding boxes with severity class and confidence score

#### 2. Hair Texture Classification — MobileNetV3
- **Architecture:** MobileNetV3 (fine-tuned in Keras)
- **Task:** Hair texture classification (straight, wavy, curly, coily)
- **Approach:** Transfer learning — pretrained ImageNet weights, custom classification head trained on hair texture dataset
- **Output:** Texture class + confidence score

#### 3. Face Shape Detection — SVM
- **Architecture:** Support Vector Machine (scikit-learn)
- **Features:** Euclidean distance ratios between MediaPipe facial landmarks (jaw width, face length, cheekbone width, forehead width)
- **Task:** Face shape classification (oval, round, square, heart, oblong)
- **Output:** Shape class + confidence score

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│                  React Frontend                  │
│            (Tailwind CSS, WebSocket)             │
└────────────────────┬────────────────────────────┘
                     │ REST / WebSocket
┌────────────────────▼────────────────────────────┐
│              Go Microservice                     │
│       Firebase JWT verification middleware       │
└────────────────────┬────────────────────────────┘
                     │ Verified requests
┌────────────────────▼────────────────────────────┐
│              Flask Backend (Python)              │
│                                                  │
│  ┌──────────────┐   ┌──────────────────────┐    │
│  │  ML Pipeline │   │   Advice Engine      │    │
│  │  - MediaPipe │   │   - Template engine  │    │
│  │  - OpenCV    │   │   - TF-IDF chatbot   │    │
│  │  - YOLOv8    │   │   - Color palettes   │    │
│  │  - MobileNet │   └──────────────────────┘    │
│  │  - SVM       │                                │
│  └──────────────┘   ┌──────────────────────┐    │
│                     │   Backend Services   │    │
│  ┌──────────────┐   │   - Progress engine  │    │
│  │  OpenWeather │   │   - Skin Twin match  │    │
│  │  UV/Humidity │   │   - APScheduler      │    │
│  │  Pollution   │   │   - FCM reminders    │    │
│  └──────────────┘   └──────────────────────┘    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│                   SQLite                         │
│        Users · Scans · Routines · History        │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Tailwind CSS |
| **Backend** | Flask (Python), Go |
| **Auth** | Firebase Google OAuth, JWT (Go middleware) |
| **Push Notifications** | Firebase Cloud Messaging, APScheduler |
| **Real-time** | Go WebSockets |
| **Database** | SQLite |
| **CV / ML** | MediaPipe, OpenCV, YOLOv8, Keras, scikit-learn |
| **External APIs** | OpenWeatherMap (UV index, humidity, pollution) |

---

## 📁 Project Structure

```
SkinMax/
├── frontend/                  # React app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
│   └── tailwind.config.js
│
├── backend/                   # Flask backend
│   ├── ml/
│   │   ├── eye_color.py       # OpenCV + MediaPipe iris analysis
│   │   ├── skin_tone.py       # LAB colorspace skin analysis
│   │   ├── acne_detector.py   # YOLOv8 inference
│   │   ├── hair_texture.py    # MobileNetV3 inference
│   │   └── face_shape.py      # SVM landmark classifier
│   ├── training/
│   │   ├── train_yolo.py      # YOLOv8 fine-tuning script
│   │   ├── train_mobilenet.py # MobileNetV3 fine-tuning script
│   │   └── train_svm.py       # SVM training script
│   ├── engine/
│   │   ├── recommender.py     # Template-based routine engine
│   │   ├── chatbot.py         # TF-IDF chatbot
│   │   ├── progress.py        # Skin health scoring
│   │   └── skin_twin.go       # Cosine similarity matching
│   ├── services/
│   │   ├── weather.py         # OpenWeatherMap integration
│   │   └── scheduler.go       # APScheduler routines
│   └── app.py                 # Flask entry point
│
├── go-auth/                   # Go JWT microservice
│   └── main.go
│
└── models/                    # Saved trained model weights
    ├── acne_yolov8.pt
    ├── hair_mobilenetv3.h5
    └── face_shape_svm.pkl
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Go 1.22+
- Firebase project (for Auth + FCM)
- OpenWeatherMap API key

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/skinmax.git
cd skinmax
```

### 2. Backend setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Go auth service
```bash
cd go-auth
go run main.go
```

### 5. Environment variables
Create a `.env` file in `/backend`:
```
OPENWEATHER_API_KEY=your_key_here
FIREBASE_CREDENTIALS=path/to/firebase.json
SECRET_KEY=your_flask_secret
```

### 6. Run the app
```bash
# In /backend
flask run

# In /frontend
npm run dev
```

---

## 👥 Team

| Name | 

| [naina] | 
| [utkarsh] | 
| [reyhan] | 
| [daksh] | 
| [shourya] | 
| [sunidhi] | 
---


<div align="center">
Built with ❤️ for CCS's Intra-Society Hackathon
</div>
