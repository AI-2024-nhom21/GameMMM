import numpy as np
import random
from game.level_manager import LevelManager
from game.player import Player
from game.enemy import Enemy
from game.learning.io import save_qtable, load_qtable
from game.var import GRID_SIZE

# Q-learning constants
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 1
EPS_MIN = 0.01
EPS_DECAY = 0.995
EPISOLES = 1000
MAX_STEPS = 200

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]
WALL, SPACE = 0, 1


def convert_level_to_board(walls, grid_size=GRID_SIZE):
    board = np.ones((grid_size, grid_size), dtype=int)
    for (r1, c1, r2, c2) in walls:
        if r1 == r2:
            row, col = r1 - 1, min(c1, c2)
        else:
            row, col = min(r1, r2), c1 - 1
        board[row, col] = WALL
    return board


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class BotAdapter(Player):
    def __init__(self, start_pos, board, walls):
        self.start_pos = start_pos
        self.pos = start_pos  # logic position (0-based)
        self.board = board
        self.walls = walls
        super().__init__([start_pos[0] + 1, start_pos[1] + 1])  # visual position (1-based)

    def reset(self):
        self.pos = self.start_pos
        self.player_pos = [self.start_pos[0] + 1, self.start_pos[1] + 1]

    def moveTo(self, new_pos):
        r, c = new_pos
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] != WALL:
            self.pos = new_pos
            self.player_pos = [r + 1, c + 1]
            return True
        return False

    def moveUp(self):
        self.direction = "up"
        return self.moveTo((self.pos[0] - 1, self.pos[1]))

    def moveDown(self):
        self.direction = "down"
        return self.moveTo((self.pos[0] + 1, self.pos[1]))

    def moveLeft(self):
        self.direction = "left"
        return self.moveTo((self.pos[0], self.pos[1] - 1))

    def moveRight(self):
        self.direction = "right"
        return self.moveTo((self.pos[0], self.pos[1] + 1))

    def findValidMoves(self):
        directions = [(self.pos[0] - 1, self.pos[1]),   # UP
                      (self.pos[0] + 1, self.pos[1]),   # DOWN
                      (self.pos[0], self.pos[1] - 1),   # LEFT
                      (self.pos[0], self.pos[1] + 1)]   # RIGHT
        valid = []
        for i, (r, c) in enumerate(directions):
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r, c] != WALL:
                valid.append(i)
        return valid


class EnemyAdapter(Enemy):
    def __init__(self, start_pos, grid_size, walls):
        super().__init__([start_pos[0] + 1, start_pos[1] + 1], grid_size, walls, enemy_type="white")
        self.start_pos = start_pos
        self.pos = start_pos

    def reset(self):
        self.pos = self.start_pos
        self.enemy_pos = [self.start_pos[0] + 1, self.start_pos[1] + 1]

    def moveTowards(self, player_pos):
        # Update internal position for movement logic
        self.enemy_pos = [self.pos[0] + 1, self.pos[1] + 1]
        new_pos = self.move_towards_player([player_pos[0] + 1, player_pos[1] + 1])
        self.pos = (new_pos[0] - 1, new_pos[1] - 1)


def train(board, player, monster, goal):
    qtable = {(r, c): [0] * 4 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r, c] != WALL}
    epsilon = EPSILON

    for episode in range(EPISOLES):
        player.reset()
        monster.reset()
        state = player.pos
        done = False
        steps = 0

        while not done and steps < MAX_STEPS:
            steps += 1
            valid_actions = player.findValidMoves()
            if not valid_actions:
                break

            if random.random() < epsilon:
                action = random.choice(valid_actions)
            else:
                action = max(valid_actions, key=lambda a: qtable[state][a])

            old_pos = state
            [player.moveUp, player.moveDown, player.moveLeft, player.moveRight][action]()
            monster.moveTowards(player.pos)
            state = player.pos

            reward = 0
            if state == goal:
                reward, done = 100, True
            elif state == monster.pos:
                reward, done = -100, True
            else:
                if get_distance(state, goal) < get_distance(old_pos, goal):
                    reward += 9
                if get_distance(state, monster.pos) < get_distance(old_pos, monster.pos):
                    reward -= 5

            old_value = qtable[old_pos][action]
            next_max = max(qtable[state]) if state in qtable else 0
            qtable[old_pos][action] = old_value + ALPHA * (reward + GAMMA * next_max - old_value)

        if epsilon > EPS_MIN:
            epsilon *= EPS_DECAY

    print("✅ Training complete.")
    return qtable


def train_all_levels():
    level_manager = LevelManager()
    for level_index in range(1, 11):
        print(f"\n🔁 Training level {level_index}...")
        level_manager.current_level = level_index
        level_data = level_manager.get_level_data()

        walls = level_data["walls"]
        board = convert_level_to_board(walls)

        player_pos = (level_data["player_pos"][0] - 1, level_data["player_pos"][1] - 1)
        monster_pos = (level_data["mummy_pos_white"][0] - 1, level_data["mummy_pos_white"][1] - 1)
        goal_pos = (level_data["stair_pos"][0] - 1, level_data["stair_pos"][1] - 1)

        player = BotAdapter(player_pos, board, walls)
        monster = EnemyAdapter(monster_pos, GRID_SIZE, walls)

        qtable = train(board.copy(), player, monster, goal_pos)
        save_qtable(level_index, qtable)
        print(f"✅ Q-table for level {level_index} saved.\n")


def test_qtable_saving_and_loading():
    for level in range(1, 11):
        qtable = load_qtable(level)
        if qtable:
            print(f"[✓] Q-table for level {level} loaded successfully. {len(qtable)} states.")
        else:
            print(f"[✗] Q-table for level {level} NOT found.")


if __name__ == "__main__":
    train_all_levels()
    test_qtable_saving_and_loading()