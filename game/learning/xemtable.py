import numpy as np

qtable = np.load("game/learning/qtable_level_1.npy", allow_pickle=True).item()

# In toàn bộ Q-table (có thể rất dài)
for state, actions in qtable.items():
    print(f"{state}: {actions}")
