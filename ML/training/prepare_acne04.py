import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ANN_DIR = "data/ACNE04/Detection/VOC2007/Annotations"
IMG_DIR = "data/ACNE04/Classification/JPEGImages"
OUTPUT  = "data/acne_yolo"

def parse_xml(xml_path, img_w, img_h):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    boxes = []
    for obj in root.findall("object"):
        bb   = obj.find("bndbox")
        xmin = int(bb.find("xmin").text)
        ymin = int(bb.find("ymin").text)
        xmax = int(bb.find("xmax").text)
        ymax = int(bb.find("ymax").text)
        cx = (xmin + xmax) / 2 / img_w
        cy = (ymin + ymax) / 2 / img_h
        bw = (xmax - xmin) / img_w
        bh = (ymax - ymin) / img_h
        boxes.append((cx, cy, bw, bh))
    return boxes

def get_severity(stem):
    s = stem.lower()
    if s.startswith("levle0"): return 0
    if s.startswith("levle1"): return 1
    if s.startswith("levle2"): return 2
    if s.startswith("levle3"): return 3
    return None

def get_img_size(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    w = int(root.find("size/width").text)
    h = int(root.find("size/height").text)
    return w, h

def prepare():
    for split in ["train", "val"]:
        Path(f"{OUTPUT}/{split}/images").mkdir(parents=True, exist_ok=True)
        Path(f"{OUTPUT}/{split}/labels").mkdir(parents=True, exist_ok=True)

    xml_files = sorted(Path(ANN_DIR).glob("*.xml"))
    print(f"Total XML files: {len(xml_files)}")

    done, skipped = 0, 0

    for i, xml_path in enumerate(xml_files):
        severity = get_severity(xml_path.stem)
        if severity is None:
            skipped += 1
            continue

        img_w, img_h = get_img_size(xml_path)
        boxes = parse_xml(xml_path, img_w, img_h)
        if not boxes:
            skipped += 1
            continue

        img_path = None
        for ext in [".jpg", ".jpeg", ".png"]:
            candidate = Path(IMG_DIR) / (xml_path.stem + ext)
            if candidate.exists():
                img_path = candidate
                break

        if img_path is None:
            skipped += 1
            continue

        split = "val" if i % 5 == 0 else "train"
        shutil.copy(img_path, f"{OUTPUT}/{split}/images/{img_path.name}")

        lbl = f"{OUTPUT}/{split}/labels/{xml_path.stem}.txt"
        with open(lbl, "w") as f:
            for cx, cy, bw, bh in boxes:
                f.write(f"{severity} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

        done += 1

    print(f"Done: {done}  Skipped: {skipped}")
    print(f"Train: {len(list(Path(OUTPUT+'/train/images').glob('*')))} images")
    print(f"Val:   {len(list(Path(OUTPUT+'/val/images').glob('*')))} images")

prepare()