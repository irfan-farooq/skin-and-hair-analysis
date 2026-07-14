import cv2
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS  = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# to get the colour
def classify_eye_color(h, s, v, L, a, b_val):
    hue   = h * 2
    sat   = s / 255
    val   = v / 255
    light = L / 255

    
    if val < 0.25 and sat < 0.4:
        return "dark_brown"
    if 180 <= hue <= 270 and sat > 0.04:
        return "blue"
    if sat < 0.18 and 0.25 <= val <= 0.80:
        return "grey"
    if 60 <= hue <= 150 and sat > 0.22:
        return "green"
    if 20 <= hue <= 45 and sat > 0.50 and val > 0.45:
        return "amber"
    if 10 <= hue <= 45 and sat > 0.25:
        return "brown"
    if 20 <= hue <= 80 and 0.10 <= sat <= 0.45:
        return "hazel"
    return "brown"

# precision estimation
def compute_confidence(iris_pixels_rgb, predicted_color):
    pixels_img = iris_pixels_rgb.reshape(-1, 1, 3).astype(np.uint8)
    pixels_hsv = cv2.cvtColor(pixels_img, cv2.COLOR_RGB2HSV)
    hsv = pixels_hsv.reshape(-1, 3)

    total = len(hsv)
    if total == 0:
        return 0.5

    color_ranges = {
        "dark_brown": (0,  20),
        "brown":      (5,  20),
        "amber":      (10, 22),
        "hazel":      (12, 37),
        "green":      (30, 75),
        "blue":       (90, 130),
        "grey":       (0,  180),
    }

    hues = hsv[:, 0]
    sats = hsv[:, 1] / 255.0

    if predicted_color == "grey":
        votes = np.sum(sats < 0.15)
    else:
        lo, hi = color_ranges.get(predicted_color, (0, 180))
        votes = np.sum((hues >= lo) & (hues <= hi))

    confidence = round(float(votes / total), 2)
    return max(0.5, min(0.98, confidence))


def detect_eye_color(image_path: str) -> dict:
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        return {"error": "Could not read image"}

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    h_img, w_img = image_rgb.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(image_rgb)

    if not results.multi_face_landmarks:
        return {"error": "No face detected"}

    landmarks = results.multi_face_landmarks[0].landmark

    def iris_info(indices):
        pts = [(int(landmarks[i].x * w_img),
                int(landmarks[i].y * h_img)) for i in indices]
        cx = sum(p[0] for p in pts) // len(pts)
        cy = sum(p[1] for p in pts) // len(pts)
        r  = abs(pts[0][0] - pts[2][0]) // 2
        return (cx, cy), r

    lc, lr = iris_info(LEFT_IRIS)
    rc, rr = iris_info(RIGHT_IRIS)

    def extract_pixels(center, radius):
        cx, cy = center
        mask = np.zeros((h_img, w_img), dtype=np.uint8)
        cv2.circle(mask, (cx, cy), radius, 255, -1)
        cv2.circle(mask, (cx, cy), int(radius * 0.45), 0, -1)
        return image_rgb[mask > 0]

    left_px  = extract_pixels(lc, lr)
    right_px = extract_pixels(rc, rr)
    all_pixels = np.vstack([left_px, right_px])

    if len(all_pixels) < 10:
        return {"error": "Iris region too small"}
    
    px_check = all_pixels.reshape(-1, 1, 3).astype(np.uint8)
    hsv_check = cv2.cvtColor(px_check, cv2.COLOR_RGB2HSV).reshape(-1, 3)

    hues_check = hsv_check[:, 0] * 2   # 0-360
    sats_check = hsv_check[:, 1] / 255
    vals_check = hsv_check[:, 2] / 255

# Remove skin pixels, eyelashes, sclera
    clean_mask = (
    (hues_check > 55) |       
    (sats_check < 0.08)        
    )
    clean_mask = clean_mask & (vals_check > 0.20) & (vals_check < 0.88)
    all_pixels = all_pixels[clean_mask]

   
    if len(all_pixels) < 10:
     clean_mask = (vals_check > 0.20) & (vals_check < 0.88)
     all_pixels = all_pixels[clean_mask]

    if len(all_pixels) < 10:
     return {"error": "Could not isolate iris pixels cleanly"}
   
    px_img = all_pixels.reshape(-1, 1, 3).astype(np.uint8)
    hsv_px = cv2.cvtColor(px_img, cv2.COLOR_RGB2HSV).reshape(-1, 3)
    lab_px = cv2.cvtColor(px_img, cv2.COLOR_RGB2LAB).reshape(-1, 3)

    h = float(np.median(hsv_px[:, 0])) * 2
    s = float(np.median(hsv_px[:, 1]))
    v = float(np.median(hsv_px[:, 2]))
    L = float(np.median(lab_px[:, 0]))

    color = classify_eye_color(h*0.5, s, v, L, 0, 0)
    confidence = compute_confidence(all_pixels, color)

    return {
        "eye_color":  color,
        "confidence": confidence,
        "hsv": {"hue": round(h, 1), "saturation": round(s/255, 3), "value": round(v/255, 3)},
        "lab": {"L": round(L/255, 3)}
    }