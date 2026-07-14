from ultralytics import YOLO

SEVERITY = ['Clear', 'Mild', 'Moderate', 'Severe']

def load_model(path="models/acne/best.pt"):
    return YOLO(path)

def detect_acne(image_path, model):
    results = model(image_path, verbose=False)[0]
    h, w = results.orig_shape
    
    detections = []
    if results.boxes is not None:
        for box in results.boxes:
            xyxy = box.xyxy[0].tolist()
            x_min, y_min, x_max, y_max = xyxy
            
            x_min_norm = x_min / w
            y_min_norm = y_min / h
            x_max_norm = x_max / w
            y_max_norm = y_max / h
            center_x = (x_min_norm + x_max_norm) / 2
            center_y = (y_min_norm + y_max_norm) / 2
            
            if center_y < 0.35:
                region = "forehead"
            elif center_y > 0.65:
                region = "chin"
            elif center_x < 0.4:
                region = "left_cheek"
            else:
                region = "right_cheek"
            
            detections.append({
                "severity": SEVERITY[int(box.cls[0])],
                "confidence": round(float(box.conf[0]) * 100, 1),
                "bbox": {
                    "x_min": round(x_min_norm, 3),
                    "y_min": round(y_min_norm, 3),
                    "x_max": round(x_max_norm, 3),
                    "y_max": round(y_max_norm, 3),
                    "center_x": round(center_x, 3),
                    "center_y": round(center_y, 3)
                },
                "region": region
            })
    
    overall = max(detections, key=lambda d: SEVERITY.index(d["severity"]))["severity"] if detections else "Clear"
    
    return {
        "overall_severity": overall,
        "detections": detections,
        "count": len(detections)
    }