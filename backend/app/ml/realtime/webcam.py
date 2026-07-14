import cv2
import sys
sys.path.insert(0, '.')
from pipeline.acne_detector import load_model

model = load_model("models/acne/best.pt")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

SEVERITY_COLORS = {
    "Clear": (0, 255, 0),
    "Mild": (0, 255, 255),
    "Moderate": (0, 165, 255),
    "Severe": (0, 0, 255)
}

frame_count = 0
results_cache = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    
    if frame_count % 5 == 0:
        h, w = frame.shape[:2]
        cv2.imwrite("temp_frame.jpg", frame)
        
        results = model("temp_frame.jpg", verbose=False)[0]
        results_cache = results
    
    if results_cache is not None:
        h, w = frame.shape[:2]
        
        if results_cache.boxes is not None:
            for box in results_cache.boxes:
                xyxy = box.xyxy[0].tolist()
                x_min, y_min, x_max, y_max = xyxy
                
                severity = ["Clear", "Mild", "Moderate", "Severe"][int(box.cls[0])]
                conf = float(box.conf[0])
                
                color = SEVERITY_COLORS.get(severity, (255, 255, 255))
                
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)
                label = f"{severity} {conf*100:.1f}%"
                cv2.putText(frame, label, (int(x_min), int(y_min)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow("SkinMax — Acne Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()