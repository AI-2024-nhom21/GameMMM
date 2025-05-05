import pygame
from game.var import WIDTH, HEIGHT, FPS, GRID_SIZE
from game.level_manager import LevelManager
from game.game_logic import GameLogic
from game.player import Player
from game.enemy import Enemy
from game.menu import Menu, MENU_PAUSE, GAME_RUNNING
from game.learning.Q_learning import BotAdapter, Point, load_qtable, coorTuplesToId, UP, DOWN, LEFT, RIGHT
import time

pygame.init()

# Cài đặt màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Khởi tạo các thành phần
menu = Menu(screen)
level_manager = LevelManager()
game_logic = GameLogic(screen)

# Biến trạng thái
running = True
clock = pygame.time.Clock()
game_active = False


last_bot_move_time = 0
bot_move_interval = 400  # milliseconds 🔧

# Hiển thị menu ban đầu
menu.draw_menu()

while running:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif menu.current_menu != GAME_RUNNING:
            result = menu.handle_menu_input(event)

            if result is False:
                running = False

            elif result is True and menu.current_menu == GAME_RUNNING:
                level_data = level_manager.get_level_data()
                player_pos = level_data["player_pos"]
                mummy_pos = level_data["mummy_pos_white"]
                stair_pos = level_data["stair_pos"]
                stair_type = level_data["stair_type"]
                walls = level_data["walls"]

                if menu.play_type == "BOT":
                    goal = (stair_pos[0] - 1, stair_pos[1] - 1)
                    qtable = load_qtable(level_manager.current_level)
                    player = BotAdapter(player_pos, GRID_SIZE, walls)
                    enemies = [Enemy(mummy_pos, GRID_SIZE, walls, enemy_type="white")]
                else:
                    player = Player(player_pos)
                    enemies = [Enemy(mummy_pos, GRID_SIZE, walls, enemy_type="white")]
                    if level_data["mummy_pos_red"]:
                        enemies.append(Enemy(level_data["mummy_pos_red"], GRID_SIZE, walls, enemy_type="red"))

                game_active = True

        elif game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu.menu_stack.append(menu.current_menu)
                    menu.current_menu = MENU_PAUSE
                    menu.selected_button = 0
                    menu.draw_menu()
                    game_active = False

                elif menu.play_type != "BOT":
                    new_pos = player.player_pos.copy()
                    if event.key == pygame.K_w:
                        new_pos[0] -= 1
                    elif event.key == pygame.K_s:
                        new_pos[0] += 1
                    elif event.key == pygame.K_a:
                        new_pos[1] -= 1
                    elif event.key == pygame.K_d:
                        new_pos[1] += 1

                    if player.move(new_pos, walls, GRID_SIZE):
                        for enemy in enemies:
                            enemy.move_towards_player(player.player_pos)

                        if len(enemies) == 2 and enemies[0].enemy_pos == enemies[1].enemy_pos:
                            print("Enemy white bị xóa do va chạm với enemy red!")
                            enemies.pop(0)

                    for enemy in enemies:
                        if player.player_pos == enemy.enemy_pos:
                            print("Game Over! Enemy đã bắt được bạn!")
                            running = False
                            break

                    if player.player_pos == stair_pos:
                        print(f"Chúc mừng! Bạn đã hoàn thành Level {level_manager.current_level}!")
                        if level_manager.next_level():
                            level_data = level_manager.get_level_data()
                            player = Player(level_data["player_pos"])
                            enemies = [Enemy(level_data["mummy_pos_white"], GRID_SIZE, level_data["walls"], enemy_type="white")]
                            if level_data["mummy_pos_red"]:
                                enemies.append(Enemy(level_data["mummy_pos_red"], GRID_SIZE, level_data["walls"], enemy_type="red"))
                            stair_pos = level_data["stair_pos"]
                            stair_type = level_data["stair_type"]
                            walls = level_data["walls"]
                            print(f"Chuyển sang Level {level_manager.current_level}")
                        else:
                            print("Chúc mừng! Bạn đã hoàn thành tất cả các cấp độ!")
                            running = False

    #BOT tự động di chuyển
    current_time = pygame.time.get_ticks()
    if menu.play_type == "BOT" and game_active and current_time - last_bot_move_time >= bot_move_interval:
        last_bot_move_time = current_time

        state = coorTuplesToId(player.pos.toTuple(), (enemies[0].enemy_pos[0], enemies[0].enemy_pos[1]))
        valid_actions = player.findValidMoves()
        state_scores = qtable[state]
        chosen_action = valid_actions[0]
        highest_score = state_scores[chosen_action]
        for action in valid_actions:
            score = state_scores[action]
            if score > highest_score:
                highest_score = score
                chosen_action = action

        if chosen_action == UP:
            player.moveUp()
        elif chosen_action == DOWN:
            player.moveDown()
        elif chosen_action == LEFT:
            player.moveLeft()
        elif chosen_action == RIGHT:
            player.moveRight()

        for enemy in enemies:
            enemy.move_towards_player(player.player_pos)

        for enemy in enemies:
            enemy_pos = Point(enemy.enemy_pos[0], enemy.enemy_pos[1])
            if player.pos.compare(enemy_pos):
                print("Game Over! Enemy đã bắt được bạn!")
                running = False
                break

        goal_pos = Point(stair_pos[0], stair_pos[1])
        if player.pos.compare(goal_pos):
            print(f"Chúc mừng! Bạn đã hoàn thành Level {level_manager.current_level}!")
            if level_manager.next_level():
                level_data = level_manager.get_level_data()
                qtable = load_qtable(level_manager.current_level)
                player = BotAdapter(level_data["player_pos"], GRID_SIZE, level_data["walls"])
                enemies = [Enemy(level_data["mummy_pos_white"], GRID_SIZE, level_data["walls"], enemy_type="white")]
                if level_data["mummy_pos_red"]:
                    enemies.append(Enemy(level_data["mummy_pos_red"], GRID_SIZE, level_data["walls"], enemy_type="red"))
                stair_pos = level_data["stair_pos"]
                stair_type = level_data["stair_type"]
                walls = level_data["walls"]
                print(f"Chuyển sang Level {level_manager.current_level}")
            else:
                print("Chúc mừng! Bạn đã hoàn thành tất cả các cấp độ!")
                running = False

    if game_active:
        player.update_animation(delta_time)
        for enemy in enemies:
            enemy.update_animation(delta_time)  # 🔧 hoạt ảnh mượt

        game_logic.draw_map(walls, stair_pos, stair_type, player, enemies)
        pygame.display.flip()

pygame.quit()