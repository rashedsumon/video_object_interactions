import kagglehub
import os

DATA_DIR = "data"
DATASET = "kmader/videoobjecttracking"

def download_dataset():
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Download and unzip the dataset
    path = kagglehub.dataset_download(
        dataset=DATASET,          # keyword argument required
        download_path=DATA_DIR,
        unzip=True                # automatically unzip
    )

    print("Dataset downloaded to:", path)
    return path

if __name__ == "__main__":
    download_dataset()
