import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pickle
import os

CHIN        = 152
LEFT_JAW    = 234
RIGHT_JAW   = 454
LEFT_TEMPLE = 127
RIGHT_TEMPLE= 356
FOREHEAD    = 10
LEFT_CHEEK  = 116
RIGHT_CHEEK = 345
LEFT_BROW   = 70
RIGHT_BROW  = 300

def _dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def extract_features(points):
    jaw     = _dist(points[LEFT_JAW],    points[RIGHT_JAW])
    cheek   = _dist(points[LEFT_CHEEK],  points[RIGHT_CHEEK])
    temple  = _dist(points[LEFT_TEMPLE], points[RIGHT_TEMPLE])
    height  = _dist(points[FOREHEAD],    points[CHIN])
    upper   = _dist(points[FOREHEAD],    points[LEFT_BROW])
    lower   = _dist(points[LEFT_BROW],   points[CHIN])

    if height == 0 or cheek == 0 or temple == 0 or lower == 0:
        return None

    return [
        jaw   / height,
        cheek / height,
        temple/ height,
        jaw   / cheek,
        cheek / temple,
        upper / lower
    ]

def _synthetic_data():
    np.random.seed(42)
    X, y = [], []
    shapes = {
        "Oval"   : [0.55, 0.65, 0.62, 0.85, 1.05, 0.45],
        "Round"  : [0.70, 0.75, 0.72, 0.93, 1.04, 0.50],
        "Square" : [0.75, 0.75, 0.76, 1.00, 0.99, 0.48],
        "Heart"  : [0.50, 0.68, 0.75, 0.74, 0.91, 0.43],
        "Oblong" : [0.52, 0.58, 0.56, 0.90, 1.04, 0.40],
        "Diamond": [0.52, 0.78, 0.60, 0.67, 1.30, 0.47],
    }
    for shape, base in shapes.items():
        for _ in range(300):
            X.append(np.array(base) + np.random.normal(0, 0.03, 6))
            y.append(shape)
    return np.array(X), np.array(y)

def train(save_path="models/face_shape.pkl"):
    X, y = _synthetic_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = SVC(kernel='rbf', C=10, gamma='scale', probability=True)
    model.fit(X_scaled, y)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        pickle.dump({"model": model, "scaler": scaler}, f)
    print(f"Saved → {save_path}")

import os

def predict(points, model_path=None):
    if model_path is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "face_shape.pkl")
    features = extract_features(points)
    if features is None:
        return {"error": "could not extract features"}
    with open(model_path, "rb") as f:
        saved = pickle.load(f)
    X = saved["scaler"].transform([features])
    pred = saved["model"].predict(X)[0]
    conf = round(float(max(saved["model"].predict_proba(X)[0])) * 100, 1)
    return {"shape": pred, "confidence": conf}