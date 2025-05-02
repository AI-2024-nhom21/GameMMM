# var.py
import os 

# Kích thước màn hình
WIDTH = 640  
HEIGHT = 480
    
# Thông tin map
GRID_SIZE = 9  # Ma trận 9x9 (không đổi)
CELL_SIZE = 42
START_X = 207
START_Y = 74

# Tốc độ khung hình
FPS = 60


# LEARNING
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.2
EPISTALL = 1000
# Đường dẫn đến tài nguyên
ASSETS_PATH = "assets/images/"
MAP_PATH = ASSETS_PATH + "map/"
BACKDROP_PATH = ASSETS_PATH + "background/"
EXPLORER_PATH = ASSETS_PATH + "explorer/"
ENEMY_RED_PATH = ASSETS_PATH + "enemy/enemy_red/"
ENEMY_WHITE_PATH = ASSETS_PATH + "enemy/enemy_white/"