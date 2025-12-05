import kagglehub
import os
import zipfile
import streamlit as st

DATA_DIR = "data"
DATASET = "kmader/videoobjecttracking"

# Set Kaggle credentials from Streamlit secrets
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

def download_dataset():
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Download the dataset (without unzip)
    zip_path = kagglehub.dataset_download(
        dataset=DATASET,
        download_path=DATA_DIR
    )

    # Unzip manually
    if zip_path.endswith(".zip"):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        print(f"Dataset downloaded and extracted to: {DATA_DIR}")
    else:
        print(f"Dataset downloaded to: {zip_path}")

    return DATA_DIR

if __name__ == "__main__":
    download_dataset()
