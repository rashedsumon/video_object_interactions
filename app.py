import streamlit as st
import cv2
import numpy as np
import tempfile
from utils.object_tracker import detect_objects, draw_objects
from utils.interaction_rules import check_interactions, plot_interaction_stats
from data_loader import download_dataset

st.set_page_config(page_title="Object Interaction Analyzer", layout="wide")
st.title("Real-Time Object Interaction Analysis")

# Download dataset
dataset_path = download_dataset()

# Video upload
video_file = st.file_uploader("Upload Video", type=["mp4", "avi"])
stframe = st.empty()

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    cap = cv2.VideoCapture(tfile.name)

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
                x11, y11, x12, y12 = obj1["box"]
                x21, y21, x22, y22 = obj2["box"]
                x1c, y1c = (x11 + x12)//2, (y11 + y12)//2
                x2c, y2c = (x21 + x22)//2, (y21 + y22)//2
                cv2.line(frame, (x1c, y1c), (x2c, y2c), (0,0,255), 2)

        stframe.image(frame, channels="BGR")

    cap.release()

st.subheader("Interaction Stats")
st.button("Plot Interaction Frequency", on_click=plot_interaction_stats)
