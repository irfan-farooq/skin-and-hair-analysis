from skintone import analyze_skin

import cv2
import mediapipe as mp
import numpy as np





mp_face_mesh = mp.solutions.face_mesh

def dark_circles(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return {"severity": "N/A"}
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    # DETECT FACE


    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            raise Exception("No face detected")

        landmarks = results.multi_face_landmarks[0].landmark


    # CONVERT LANDMARKS TO DICT
    # (needed by skintone.py)


    h, w = image.shape[:2]

    points = {}

    for idx, lm in enumerate(landmarks):
        x = int(lm.x * w)
        y = int(lm.y * h) 

        points[idx] = (x, y)


    # SKIN ANALYSIS


    skin_result = analyze_skin(image, points)

    skin_L = skin_result["lab"]["L"]
    skin_a = skin_result["lab"]["a"]
    skin_b = skin_result["lab"]["b"]

    print("Skin LAB:", skin_L, skin_a, skin_b)


    # UNDER-EYE REGIONS


    LEFT_UNDER_EYE = [
        133,155,154,153,145
    ]

    RIGHT_UNDER_EYE = [
        362,390,373,374,380
    ]


    # REGION EXTRACTION

    def get_region(image, landmarks, indices):

        h, w = image.shape[:2]

        upper_pts = []

        for idx in indices:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)

            upper_pts.append([x, y])

        upper_pts = np.array(upper_pts)

        # Create lower boundary directly below each point
        lower_pts = []

        for x, y in reversed(upper_pts):
            lower_pts.append([x, y + int(h * 0.04)])

        pts = np.vstack([upper_pts, lower_pts]).astype(np.int32)

        mask = np.zeros((h, w), dtype=np.uint8)

        cv2.fillConvexPoly(mask, pts, 255)

        region = cv2.bitwise_and(image, image, mask=mask)

        return region, mask, pts


    # EXTRACT EYES


    left_eye_region, left_eye_mask, left_pts = get_region(
        image,
        landmarks,
        LEFT_UNDER_EYE
    )

    right_eye_region, right_eye_mask, right_pts = get_region(
        image,
        landmarks,
        RIGHT_UNDER_EYE
    )



    # -----------------------------
    # LAB CALCULATION
    # -----------------------------

    def mean_lab(region, mask):

        lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)

        pixels = lab[mask > 0]

        L = pixels[:,0].mean()
        a = pixels[:,1].mean() - 128
        b = pixels[:,2].mean() - 128

        return L, a, b

    left_L, left_a, left_b = mean_lab(
        left_eye_region,
        left_eye_mask
    )

    right_L, right_a, right_b = mean_lab(
        right_eye_region,
        right_eye_mask
    )

    eye_L = (left_L + right_L) / 2
    eye_a = (left_a + right_a) / 2
    eye_b = (left_b + right_b) / 2

    # -----------------------------
    # DARK CIRCLE SCORE
    # -----------------------------

    lightness_drop = skin_L - eye_L

    color_distance = np.sqrt(
        (skin_L - eye_L) ** 2 +
        (skin_a - eye_a) ** 2 +
        (skin_b - eye_b) ** 2
    )

    severity_score = (
        0.7 * lightness_drop +
        0.3 * color_distance
    )

    # -----------------------------
    # CLASSIFICATION
    # -----------------------------

    if severity_score < 4:
        severity = "None"

    elif severity_score < 8:
        severity = "Mild"

    elif severity_score < 20:
        severity = "Moderate"

    else:
        severity = "Severe"


 
    return {

        "severity": severity,

        "severity_score": round(float(severity_score), 2),

        "lightness_drop": round(float(lightness_drop), 2),

        "color_distance": round(float(color_distance), 2)

    }