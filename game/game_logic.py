# game_logic.py

import pygame
from game.var import MAP_PATH, START_X, START_Y, CELL_SIZE, BACKDROP_PATH

class GameLogic:
    def __init__(self, screen):
        self.screen = screen
        self.backdrop_image = pygame.image.load(BACKDROP_PATH + "backdrop2.png")
        self.backdrop_image = pygame.transform.scale(self.backdrop_image, (640, 480))
        self.map_image = pygame.image.load(MAP_PATH + "matrix.png")
        self.map_image = pygame.transform.scale(self.map_image, (485, 480))
        self.wall_vertical = pygame.transform.scale(pygame.image.load(MAP_PATH + "wall_part_1.png"), (8, 45))
        self.wall_horizontal = pygame.transform.scale(pygame.image.load(MAP_PATH + "wall_part_2.png"), (45, 8))
        self.stair_ud = pygame.transform.scale(pygame.image.load(MAP_PATH + "stairs_UD.png"), (CELL_SIZE, CELL_SIZE))
        self.stair_lr = pygame.transform.scale(pygame.image.load(MAP_PATH + "stairs_LR.png"), (CELL_SIZE, CELL_SIZE))
        self.walls = []  # Danh sách tường
        self.stair_pos = (0, 0)  # Vị trí cầu thang
        self.stair_type = "UD"  # Loại cầu thang
        self.player = None  # Đối tượng người chơi
        self.enemies = []  # Danh sách kẻ thù
        self.player_move_history = []  # Lịch sử di chuyển của người chơi
        self.enemy_move_histories = []  # Lịch sử di chuyển của từng kẻ thù
        self.initial_player_pos = None  # Vị trí ban đầu của người chơi
        self.initial_enemy_pos = []  # Vị trí ban đầu của kẻ thù

    def set_game_state(self, walls, stair_pos, stair_type, player, enemies):
        """Thiết lập trạng thái game"""
        self.walls = walls
        self.stair_pos = stair_pos
        self.stair_type = stair_type
        self.player = player
        self.enemies = enemies
        self.player_move_history = []
        self.enemy_move_histories = [[] for _ in enemies]
        self.initial_player_pos = list(player.player_pos) if player and hasattr(player, 'player_pos') else None
        self.initial_enemy_pos = [list(enemy.enemy_pos) for enemy in enemies] if enemies else []

    def save_move(self):
        """Lưu vị trí hiện tại của player và enemies vào lịch sử"""
        if self.player and hasattr(self.player, 'player_pos'):
            self.player_move_history.append(list(self.player.player_pos))
        for i, enemy in enumerate(self.enemies):
            self.enemy_move_histories[i].append(list(enemy.enemy_pos))

    def undo_move(self):
        """Hoàn tác di chuyển trước đó của player và enemies"""
        if self.player and len(self.player_move_history) > 1:
            self.player_move_history.pop()  # Xóa vị trí hiện tại
            self.player.player_pos = list(self.player_move_history[-1])  # Khôi phục vị trí trước
        for i, enemy in enumerate(self.enemies):
            if len(self.enemy_move_histories[i]) > 1:
                self.enemy_move_histories[i].pop()  # Xóa vị trí hiện tại
                enemy.enemy_pos = list(self.enemy_move_histories[i][-1])  # Khôi phục vị trí trước

    def reset_move(self):
        """Đặt lại vị trí của player và enemies về vị trí ban đầu"""
        if self.player and self.initial_player_pos:
            self.player.player_pos = list(self.initial_player_pos)
            self.player_move_history = [list(self.initial_player_pos)]
        for i, enemy in enumerate(self.enemies):
            if i < len(self.initial_enemy_pos):
                enemy.enemy_pos = list(self.initial_enemy_pos[i])
                self.enemy_move_histories[i] = [list(self.initial_enemy_pos[i])]

    def draw_map(self, walls, stair_pos, stair_type, player, enemies):
        """Vẽ toàn bộ map, bao gồm tường, cầu thang, player, enemies và khung xanh cho nước đi cũ"""
        self.screen.blit(self.backdrop_image, (0, 0))
        map_x = 151
        map_y = 4
        self.screen.blit(self.map_image, (map_x, map_y))
        #vẽ khung xanh lá cây cho các bước đi cũ của người chơi
        for move in self.player_move_history[:-1]:  # Bỏ qua bước đi hiện tại
            old_x = START_X + (move[1] - 1) * CELL_SIZE
            old_y = START_Y + (move[0] - 1) * CELL_SIZE
            pygame.draw.rect(self.screen, (0, 255, 0), (old_x, old_y, CELL_SIZE, CELL_SIZE), 3)  # Khung xanh, viền 3px

        # Vẽ khung đỏ cho các bước đi cũ của từng kẻ thù
        for i, enemy_history in enumerate(self.enemy_move_histories):
            for move in enemy_history[:-1]:  # Bỏ qua bước đi hiện tại
                old_x = START_X + (move[1] - 1) * CELL_SIZE
                old_y = START_Y + (move[0] - 1) * CELL_SIZE
                pygame.draw.rect(self.screen, (255, 0, 0), (old_x, old_y, CELL_SIZE, CELL_SIZE), 3)  # Khung xanh, viền 3px

        # Vẽ tường
        for wall in walls:
            row1, col1, row2, col2 = wall
            if row1 == row2:
                x = START_X + col1 * CELL_SIZE
                y = START_Y + (row1 - 1) * CELL_SIZE
                self.screen.blit(self.wall_vertical, (x, y))
            else:
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

        # Vẽ người chơi và kẻ thù
        player.draw(self.screen, START_X, START_Y)
        for enemy in enemies:
            enemy.draw(self.screen, START_X, START_Y)