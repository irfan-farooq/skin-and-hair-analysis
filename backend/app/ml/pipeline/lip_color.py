import cv2
import numpy as np

LIP_INDICES = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 146, 91, 181, 84, 17, 314, 405, 321, 375]

def _sample(img, points, indices, margin=3):
    h, w = img.shape[:2]
    pixels = []
    for i in indices:
        if i not in points:
            continue
        x, y = points[i]
        patch = img[max(0,y-margin):min(h,y+margin), max(0,x-margin):min(w,x+margin)]
        if patch.size:
            pixels.extend(patch.reshape(-1, 3).tolist())
    return np.array(pixels, dtype=np.uint8) if pixels else None

def analyze_lip(img, points):
    pixels = _sample(img, points, LIP_INDICES)
    if pixels is None:
        return {"error": "no lip pixels sampled"}

    hsv = cv2.cvtColor(pixels.reshape(1, -1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    H, S, V = hsv.mean(axis=0)

    if S < 40:
        color = "Nude/Pale"
    elif V < 80:
        color = "Deep Berry"
    elif H < 10 or H > 160:
        color = "Classic Red"
    elif H < 20:
        color = "Coral"
    else:
        color = "Rosy Pink"

    mean_bgr = pixels.mean(axis=0)
    hex_color = "#{:02x}{:02x}{:02x}".format(int(mean_bgr[2]), int(mean_bgr[1]), int(mean_bgr[0]))

    return {"color": color, "hex": hex_color}