# level_4.py

player_pos = [1, 1]
mummy_pos_white = [3, 6]  # Enemy White
stair_pos = [6, 6]
stair_type = "LR"
entry_direction = "left"
walls = [
    (1, 2, 2, 2), (2, 3, 2, 4), (3, 1, 4, 1), (3, 3, 3, 4),
    (4, 2, 5, 2), (5, 3, 6, 3), (6, 4, 6, 5), (2, 5, 3, 5),
    (4, 4, 4, 5), (5, 5, 5, 6),
    (5, 6, 6, 6), (6, 6, 7, 6), (6, 6, 6, 7)
]