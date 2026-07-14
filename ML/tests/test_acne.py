import sys
sys.path.insert(0, '.')

from pipeline.acne_detector import load_model, detect_acne
import cv2

model = load_model("models/acne/best.pt")
image_path = "tests/images/sample.jpg"
result = detect_acne(image_path, model)

# Draw boxes on image
img = cv2.imread(image_path)
h, w = img.shape[:2]

for detection in result["detections"]:
    bbox = detection["bbox"]
    x_min = int(bbox["x_min"] * w)
    y_min = int(bbox["y_min"] * h)
    x_max = int(bbox["x_max"] * w)
    y_max = int(bbox["y_max"] * h)
    
    severity = detection["severity"]
    conf = detection["confidence"]
    
    # Color based on severity
    colors = {"Clear": (0, 255, 0), "Mild": (0, 255, 255), "Moderate": (0, 165, 255), "Severe": (0, 0, 255)}
    color = colors.get(severity, (255, 255, 255))
    
    # Draw box
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
    # Draw label
    label = f"{severity} {conf}%"
    cv2.putText(img, label, (x_min, y_min-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Save annotated image
cv2.imwrite("outputs/acne_detection.jpg", img)
print(f"✓ Annotated image saved to outputs/acne_detection.jpg")
print(f"Result: {result}")