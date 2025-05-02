# level_manager.py

from game.level_map import level_1
from game.level_map import level_2
from game.level_map import level_3
from game.level_map import level_4
from game.level_map import level_5
from game.level_map import level_6
from game.level_map import level_7
from game.level_map import level_8
from game.level_map import level_9
from game.level_map import level_10

# Danh sách các file cấp độ
LEVELS = {
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5,
    6: level_6,
    7: level_7,
    8: level_8,
    9: level_9,
    10: level_10
}

class LevelManager:
    def __init__(self):
        self.current_level = 1  # Bắt đầu từ Level 1
        self.max_level = max(LEVELS.keys())  # Cấp độ tối đa (hiện tại là 10)

    def get_level_data(self):
        """Lấy dữ liệu của cấp độ hiện tại"""
        level_data = LEVELS.get(self.current_level)
        if not level_data:
            raise ValueError(f"Không tìm thấy dữ liệu cho cấp độ {self.current_level}")
        # Kiểm tra xem cấp độ có mummy_pos_red hay không
        mummy_pos_red = getattr(level_data, "mummy_pos_red", None)
        return {
            "player_pos": level_data.player_pos,
            "mummy_pos_white": level_data.mummy_pos_white,  # Enemy White (tất cả cấp độ)
            "mummy_pos_red": mummy_pos_red,  # Enemy Red (từ Level 8)
            "stair_pos": level_data.stair_pos,
            "stair_type": level_data.stair_type,
            "entry_direction": level_data.entry_direction,
            "walls": level_data.walls
        }

    def next_level(self):
        """Chuyển sang cấp độ tiếp theo"""
        self.current_level += 1
        if self.current_level > self.max_level:
            self.current_level = 1  # Quay lại Level 1 nếu đã hoàn thành Level 10
            return False  # Trả về False để báo hiệu đã hoàn thành tất cả cấp độ
        return True  # Trả về True nếu vẫn còn cấp độ để chơi
    
