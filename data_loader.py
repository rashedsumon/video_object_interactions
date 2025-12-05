import os
import zipfile
import streamlit as st
import kagglehub

DATA_DIR = "data"
DATASET = "kmader/videoobjecttracking"

def download_dataset():
    # -----------------------------
    # Set Kaggle credentials
    # -----------------------------
    KAGGLE_USERNAME = st.secrets.get("KAGGLE_USERNAME", os.environ.get("KAGGLE_USERNAME"))
    KAGGLE_KEY = st.secrets.get("KAGGLE_KEY", os.environ.get("KAGGLE_KEY"))

    if not KAGGLE_USERNAME or not KAGGLE_KEY:
        st.error("Kaggle API credentials not found. Please set them in Streamlit secrets or environment variables.")
        st.stop()

    os.environ["KAGGLE_USERNAME"] = KAGGLE_USERNAME
    os.environ["KAGGLE_KEY"] = KAGGLE_KEY

    # -----------------------------
    # Ensure data directory exists
    # -----------------------------
    os.makedirs(DATA_DIR, exist_ok=True)

    # -----------------------------
    # Download dataset
    # -----------------------------
    zip_path = kagglehub.dataset_download(dataset=DATASET, download_path=DATA_DIR)

    # Unzip manually
    if zip_path.endswith(".zip"):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        st.success(f"Dataset downloaded and extracted to: {DATA_DIR}")
    else:
        st.success(f"Dataset downloaded to: {zip_path}")

    return DATA_DIR

if __name__ == "__main__":
    download_dataset()
