# game_logic.py

import pygame
from game.var import MAP_PATH, START_X, START_Y, CELL_SIZE, BACKDROP_PATH

class GameLogic:
    def __init__(self, screen):
        self.screen = screen

        self.backdrop_image = pygame.image.load(BACKDROP_PATH + "backdrop2.png")
        self.backdrop_image = pygame.transform.scale(self.backdrop_image, (640, 480))  # Đúng kích thước phông nền

        self.map_image = pygame.image.load(MAP_PATH + "matrix.png")
        self.map_image = pygame.transform.scale(self.map_image, (485, 480))  # Đúng kích thước bản đồ
 
        self.wall_vertical = pygame.transform.scale(pygame.image.load(MAP_PATH + "wall_part_1.png"), (8, 45))  # Giảm từ 10x80 xuống 8x60
        self.wall_horizontal = pygame.transform.scale(pygame.image.load(MAP_PATH + "wall_part_2.png"), (45, 8))  # Giảm từ 80x10 xuống 60x8
        
        self.stair_ud = pygame.transform.scale(pygame.image.load(MAP_PATH + "stairs_UD.png"), (CELL_SIZE, CELL_SIZE))  # Giảm từ 80x80 xuống 60x60
        self.stair_lr = pygame.transform.scale(pygame.image.load(MAP_PATH + "stairs_LR.png"), (CELL_SIZE, CELL_SIZE))  # Giảm từ 80x80 xuống 60x60

    def draw_map(self, walls, stair_pos, stair_type, player, enemies):
        """Vẽ toàn bộ map, bao gồm tường, cầu thang, player và enemies"""
        # Vẽ phông nền
        self.screen.blit(self.backdrop_image, (0, 0))

        # Vẽ map (căn giữa backdrop)
        map_x = 151 # Tọa độ X để căn giữa
        map_y = 4 # Tọa độ Y để căn giữa
        self.screen.blit(self.map_image, (map_x, map_y))
        # Vẽ tường
        for wall in walls:
            row1, col1, row2, col2 = wall
            if row1 == row2:  # Tường dọc
                x = START_X + col1 * CELL_SIZE
                y = START_Y + (row1 - 1) * CELL_SIZE
                self.screen.blit(self.wall_vertical, (x, y))
            else:  # Tường ngang
                x = START_X + (col1 - 1) * CELL_SIZE
                y = START_Y + row1 * CELL_SIZE
                self.screen.blit(self.wall_horizontal, (x, y))

        # Vẽ cầu thang
        stair_x = START_X + (stair_pos[1] - 1) * CELL_SIZE
        stair_y = START_Y + (stair_pos[0] - 1) * CELL_SIZE
        if stair_type == "UD":
            self.screen.blit(self.stair_ud, (stair_x, stair_y))
        elif stair_type == "LR":
            self.screen.blit(self.stair_lr, (stair_x, stair_y))

        # Vẽ player và enemies
        player.draw(self.screen, START_X, START_Y)
        for enemy in enemies:  # Vẽ từng enemy trong danh sách
            enemy.draw(self.screen, START_X, START_Y)