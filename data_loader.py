import os
import streamlit as st

# Path to your uploaded dataset folder in Streamlit Cloud
DATA_DIR = "data/videoobjecttracking"  # make sure to upload this folder in your app

def download_dataset():
    """
    Check that the dataset exists locally and return the path.
    """
    if not os.path.exists(DATA_DIR):
        st.error(f"Dataset not found! Please upload the dataset folder to {DATA_DIR}.")
        st.stop()
    st.success(f"Dataset ready at {DATA_DIR}")
    return DATA_DIR

if __name__ == "__main__":
    download_dataset()
