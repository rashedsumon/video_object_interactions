import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Store interaction logs
interaction_log = []

def check_interactions(boxes, proximity_threshold=50):
    interactions = []
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            x1a, y1a, x2a, y2a = boxes[i]["box"]
            x1b, y1b, x2b, y2b = boxes[j]["box"]
            
            # Compute center points
            center_a = ((x1a+x2a)//2, (y1a+y2a)//2)
            center_b = ((x1b+x2b)//2, (y1b+y2b)//2)
            
            dist = np.linalg.norm(np.array(center_a)-np.array(center_b))
            if dist < proximity_threshold:
                interactions.append((boxes[i]["label"], boxes[j]["label"]))
                interaction_log.append({"pair": (boxes[i]["label"], boxes[j]["label"]), "distance": dist})
    return interactions

def plot_interaction_stats():
    counts = defaultdict(int)
    for log in interaction_log:
        counts[log["pair"]] += 1
    
    pairs = list(counts.keys())
    freqs = list(counts.values())
    
    plt.figure(figsize=(8,4))
    plt.bar([f"{p[0]}-{p[1]}" for p in pairs], freqs, color='skyblue')
    plt.title("Interaction Frequency")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
