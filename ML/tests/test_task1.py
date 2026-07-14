import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.landmarks import get_landmarks, save_debug
from pipeline.skin_tone import analyze_skin

img, points = get_landmarks("tests/images/image_1.jpg")

if points is None:
    print("No face detected")
else:
    os.makedirs("outputs", exist_ok=True)
    save_debug(img, points)
    print(analyze_skin(img, points))