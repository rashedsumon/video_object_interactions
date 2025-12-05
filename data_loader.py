

## **5️⃣ data_loader.py**


import kagglehub
import os

DATA_DIR = "data"
DATASET = "kmader/videoobjecttracking"

def download_dataset():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    path = kagglehub.dataset_download(DATASET, download_path=DATA_DIR)
    print("Dataset downloaded to:", path)
    return path

if __name__ == "__main__":
    download_dataset()
