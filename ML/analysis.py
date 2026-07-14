import sys, os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from pipeline.landmarks import get_landmarks
from pipeline.skin_tone import analyze_skin
from pipeline.lip_color import analyze_lip
from pipeline.face_shape import predict as predict_face_shape
from pipeline.acne_detector import load_model as load_acne_model, detect_acne

from completeec import detect_eye_color
from model import detect_hair_texture
from darkcircle import dark_circles

def analyze_face(image_path: str) -> dict:
    """
    We are combining our ML results here. The skin tone, lip color, acne coordinates 
    so that it can be rendered on 3D model, and face_shape, eye_colour, darkcircles, and hair type.
    """
    
    img, points = get_landmarks(image_path)
    if points is None:
        return {"error": "No face detected"}
    
    skin_result = analyze_skin(img, points)
    lip_result = analyze_lip(img, points)
    face_shape_result = predict_face_shape(points)
    
    acne_model = load_acne_model(os.path.join(BASE_DIR, "models/acne/best.pt"))
    acne_result = detect_acne(image_path, acne_model)
    
    eye_result = detect_eye_color(image_path)
    hair_result = detect_hair_texture(image_path)
    dark_circles_result = dark_circles(image_path)

    return {
        "skin": {
            "tone": skin_result.get("tone"),
            "undertone": skin_result.get("undertone"),
            "hex": skin_result.get("hex"),
            "lab": skin_result.get("lab")
        },
        "lip_color": {
            "color": lip_result.get("color"),
            "hex": lip_result.get("hex")
        },
        "face_shape": {
            "shape": face_shape_result.get("shape"),
            "confidence": face_shape_result.get("confidence")
        },
        "acne": {
            "overall_severity": acne_result.get("overall_severity"),
            "count": acne_result.get("count"),
            "detections": acne_result.get("detections")
        },
        "eye_color": {
            "color": eye_result.get("eye_color")
        },
        "hair_texture": {
            "type": hair_result.get("hair_texture")
        },
        "dark_circles": {
            "severity": dark_circles_result.get("severity")
        }
    }

if __name__ == "__main__":
    test_image = os.path.join(BASE_DIR, "tests/images/sample.jpg")
    result = analyze_face(test_image)
    print(json.dumps(result, indent=2))