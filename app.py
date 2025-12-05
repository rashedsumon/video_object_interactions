import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import zipfile

from utils.object_tracker import detect_objects, draw_objects
from utils.interaction_rules import check_interactions, plot_interaction_stats
import kagglehub

# -------------------------------
# Config
# -------------------------------
st.set_page_config(page_title="Object Interaction Analyzer", layout="wide")
st.title("Real-Time Object Interaction Analysis")

DATA_DIR = "data"
DATASET = "kmader/videoobjecttracking"

# -------------------------------
# Set Kaggle credentials from Streamlit Secrets
# -------------------------------
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

# -------------------------------
# Download Dataset
# -------------------------------
def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)

    zip_path = kagglehub.dataset_download(dataset=DATASET, download_path=DATA_DIR)

    if zip_path.endswith(".zip"):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        st.success(f"Dataset downloaded and extracted to: {DATA_DIR}")
    else:
        st.success(f"Dataset downloaded to: {zip_path}")

    return DATA_DIR

dataset_path = download_dataset()

# -------------------------------
# Video Upload
# -------------------------------
video_file = st.file_uploader("Upload Video", type=["mp4", "avi"])
stframe = st.empty()

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        boxes = detect_objects(frame)
        interactions = check_interactions(boxes)
        frame = draw_objects(frame, boxes)

        # Draw interaction lines
        for pair in interactions:
            obj1 = next((b for b in boxes if b["label"] == pair[0]), None)
            obj2 = next((b for b in boxes if b["label"] == pair[1]), None)
            if obj1 and obj2:
                x11, y11, x12, y12 = obj1["box"]
                x21, y21, x22, y22 = obj2["box"]
                x1c, y1c = (x11 + x12)//2, (y11 + y12)//2
                x2c, y2c = (x21 + x22)//2, (y21 + y22)//2
                cv2.line(frame, (x1c, y1c), (x2c, y2c), (0,0,255), 2)

        stframe.image(frame, channels="BGR")

    cap.release()

# -------------------------------
# Interaction Stats
# -------------------------------
st.subheader("Interaction Stats")
st.button("Plot Interaction Frequency", on_click=plot_interaction_stats)
