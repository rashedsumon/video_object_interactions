import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Use YOLOv8 nano for speed, change if needed

# Target objects to track (adjust based on dataset labels)
TARGET_OBJECTS = ["person", "car", "bicycle", "dog"]  

def detect_objects(frame):
    results = model(frame)[0]
    boxes = []
    for r in results.boxes:
        x1, y1, x2, y2 = map(int, r.xyxy[0])
        conf = float(r.conf[0])
        cls = int(r.cls[0])
        label = model.names[cls]
        if label in TARGET_OBJECTS:
            boxes.append({
                "label": label,
                "box": (x1, y1, x2, y2),
                "conf": conf
            })
    return boxes

def draw_objects(frame, boxes):
    for obj in boxes:
        x1, y1, x2, y2 = obj["box"]
        label = obj["label"]
        color = (0, 255, 0)  # Green boxes
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame
