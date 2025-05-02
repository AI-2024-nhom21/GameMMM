#io.py
import os
import numpy as np

# Đường dẫn trực tiếp trong thư mục game/learning/
SAVE_DIR = os.path.join("game", "learning")

def save_qtable(level_number, qtable):
    filepath = os.path.join(SAVE_DIR, f"qtable_level_{level_number}.npy")
    np.save(filepath, qtable)

def load_qtable(level_number):
    filepath = os.path.join(SAVE_DIR, f"qtable_level_{level_number}.npy")
    if os.path.exists(filepath):
        return np.load(filepath, allow_pickle=True).item()
    return None