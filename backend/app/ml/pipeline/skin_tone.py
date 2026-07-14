# pipeline/skin_tone.py
import cv2
import numpy as np

SKIN_INDICES = [
    10, 338, 297, 332, 284,        
    234, 93, 132, 58, 172,         
    454, 323, 361, 288, 397        
]

def _sample(img, points, indices, margin=4):
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

def analyze_skin(img, points):
    pixels = _sample(img, points, SKIN_INDICES)
    if pixels is None:
        return {"error": "no skin pixels sampled"}

    lab = cv2.cvtColor(pixels.reshape(1, -1, 3), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    L, a, b = lab.mean(axis=0)
    L = L / 255 * 100    
    a = a - 128    
    b_true = b - 128

    if   L > 75: tone = "Very Light"
    elif L > 65: tone = "Light"
    elif L > 55: tone = "Light-Medium"
    elif L > 45: tone = "Medium"
    elif L > 35: tone = "Medium-Dark"
    else:        tone = "Dark"

    if   b > 8: undertone = "Warm"
    elif b < 2: undertone = "Cool"
    else:        undertone = "Neutral"

    r, g, b_ch = pixels.mean(axis=0)[2], pixels.mean(axis=0)[1], pixels.mean(axis=0)[0]
    hex_color = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b_ch))

    return {
        "tone": tone,
        "undertone": undertone,
        "hex": hex_color,
        "lab": {"L": round(float(L), 2), "a": round(float(a), 2), "b": round(float(b), 2)}
    }