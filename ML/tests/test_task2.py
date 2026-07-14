import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.landmarks import get_landmarks
from pipeline.lip_color import analyze_lip
from pipeline.face_shape import train, predict

img, points = get_landmarks("tests/images/image_1.jpg")

print("img:", img is not None)
print("points:", points is not None)

print("Lip:", analyze_lip(img, points))

if not os.path.exists("models/face_shape.pkl"):
    train()

print("Face Shape:", predict(points))