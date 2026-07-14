import mediapipe as mp
import cv2

_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

def get_landmarks(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot load: {image_path}")
    h, w = img.shape[:2]
    results = _face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return img, None
    lm = results.multi_face_landmarks[0].landmark
    points = {i: (int(p.x * w), int(p.y * h)) for i, p in enumerate(lm)}
    return img, points

def save_debug(img, points, path="outputs/debug.jpg"):
    out = img.copy()
    for x, y in points.values():
        cv2.circle(out, (x, y), 1, (0, 255, 0), -1)
    cv2.imwrite(path, out)