import streamlit as st
import cv2
from utils.object_tracker import detect_objects, draw_objects
from utils.interaction_rules import check_interactions, plot_interaction_stats
from data_loader import download_dataset
import tempfile
import numpy as np

st.set_page_config(page_title="Object Interaction Analyzer", layout="wide")

st.title("Real-Time Object Interaction Analysis")

# Download dataset
dataset_path = download_dataset()

# Video upload or camera
video_file = st.file_uploader("Upload Video", type=["mp4", "avi"])
use_camera = st.checkbox("Use Webcam")

if video_file or use_camera:
    if use_camera:
        cap = cv2.VideoCapture(0)
    else:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        cap = cv2.VideoCapture(tfile.name)

    stframe = st.image([])

    while cap.isOpened():
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
                x1, y1, x2, y2 = obj1["box"]
                x1c, y1c = (x1+x2)//2, (y1+y2)//2
                x2, y2, x2b, y2b = obj2["box"]
                x2c, y2c = (x2+x2b)//2, (y2+y2b)//2
                cv2.line(frame, (x1c, y1c), (x2c, y2c), (0,0,255), 2)

        stframe.image(frame, channels="BGR")
    cap.release()

st.subheader("Interaction Stats")
st.button("Plot Interaction Frequency", on_click=plot_interaction_stats)
