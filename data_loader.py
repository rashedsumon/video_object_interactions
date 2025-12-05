import os
import zipfile
import streamlit as st
import urllib.request

DATA_DIR = "data"
DATASET_URL = "https://github.com/kmader/videoobjecttracking/archive/refs/heads/master.zip"  # Example public link

def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)

    zip_path = os.path.join(DATA_DIR, "dataset.zip")
    
    # Download if not exists
    if not os.path.exists(zip_path):
        st.info("Downloading dataset...")
        urllib.request.urlretrieve(DATASET_URL, zip_path)
        st.success("Dataset downloaded!")

    # Extract
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
    st.success(f"Dataset extracted to: {DATA_DIR}")

    return DATA_DIR

if __name__ == "__main__":
    download_dataset()
