import numpy as np
import random
from game.level_manager import LevelManager
from game.player import Player
from game.enemy import Enemy
from game.learning.io import save_qtable, load_qtable
from game.var import GRID_SIZE
import copy

# Q-learning constants
ALPHA = 0.1
GAMMA = 0.99
EPSILON = 1
EPS_MIN = 0.01
EPS_DECAY = 0.995
EPISOLES = 1000
MAX_STEPS = 200

EXPLORE = 0
EXPLOIT = 1

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]
WALL, SPACE = 0, 1

WIN_SCORE = 600
LOOSE_SCORE = -300

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def toTuple(self):
        return (self.row, self.col)

    def compare(self, other):
        return self.row == other.row and self.col == other.col

def getReward(playerPos, goalPos, enemyPos, goalDis, monsterDis, path, monsterFight = 0):
    point = 0
    if playerPos.compare(goalPos) == True:
        return WIN_SCORE
    elif playerPos.compare(enemyPos) == True:
        return LOOSE_SCORE
    else:
        if goalDis[1] < goalDis[0]:
            # point += 30
            point += 20
        elif goalDis[1] > goalDis[0]:
            point += -25
        if monsterDis[1] < monsterDis[0]:
            point += -10
    
    tPlayerPos = playerPos.toTuple()
    if tPlayerPos in path:
        point += -100
    else:
        path.append(tPlayerPos)

    return point

def getDistance(pos1, pos2):
    # manhattan
    return abs(pos2.row - pos1.row) + abs(pos2.col - pos1.col)

def generateQtable(N):
    # 1 monster for now
    spaces = []
    shape = N
    for row in range(1, shape + 1):
        for col in range(1, shape + 1):
            spaces.append((row, col))

    qtable = {} # {state: [scores for up/down/lef/right]}
    for playerPos in spaces:
        for monsterPos in spaces:
            # state = (playerPos, monsterPos)
            state = coorTuplesToId(playerPos, monsterPos)
            scores = [0] * 4
            qtable[state] = scores
    
    return qtable

def coorTuplesToId(coorTup1, coorTup2):
    # row and col is from 0 to 100
    num1, num2 = coorTup1
    num3, num4 = coorTup2
    nums = [num1, num2, num3, num4]
    resultId = 0
    for num in nums:
        resultId = resultId * 100 + num
    return resultId

def idToCoorTuples(id):
    nums = []
    while(id > 0):
        nums.append(id % 100)
        id //= 100
    return ((nums[3], nums[2]), (nums[1], nums[0]))

def actionIdToString(actionId):
    idMap = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}
    return idMap[actionId]

class BotAdapter(Player):
    def __init__(self, startPos, gridSize, walls):
        temp = Point(startPos[0], startPos[1])
        self.startPos = temp
        self.pos = copy.copy(temp)
        self.walls = walls
        self.gridSize = gridSize
        super().__init__([temp.row, temp.col])  # visual position (1-based)

    def reset(self):
        self.pos = copy.copy(self.startPos)
        self.player_pos = [self.pos.row, self.pos.col]

    def moveTo(self, newPos):
        return super().move(newPos, self.walls, self.gridSize)

    def moveUp(self):
        newPos = [self.pos.row - 1, self.pos.col]
        result = self.moveTo(newPos)
        if result:
            self.pos.row -= 1
        return result

    def moveDown(self):
        newPos = [self.pos.row + 1, self.pos.col]
        result = self.moveTo(newPos)
        if result:
            self.pos.row += 1
        return result

    def moveLeft(self):
        newPos = [self.pos.row, self.pos.col - 1]
        result = self.moveTo(newPos)
        if result:
            self.pos.col -= 1
        return result

    def moveRight(self):
        newPos = [self.pos.row, self.pos.col + 1]
        result = self.moveTo(newPos)
        if result:
            self.pos.col += 1
        return result

    def findValidMoves(self):
        results = []
        originalPos = copy.copy(self.pos)
        directions = {UP: self.moveUp, DOWN: self.moveDown, LEFT: self.moveLeft, RIGHT: self.moveRight}
        for direct, moveFunc in directions.items():
            if moveFunc():
                results.append(direct)
                self.moveTo([originalPos.row, originalPos.col])
                self.pos = copy.copy(originalPos)
        return results



class EnemyAdapter(Enemy):
    def __init__(self, startPos, gridSize, walls):
        temp = Point(startPos[0], startPos[1])
        self.startPos = temp
        self.pos = copy.copy(temp)
        super().__init__([temp.row, temp.col], gridSize, walls, "white")

    def reset(self):
        self.pos = copy.copy(self.startPos)
        self.enemy_pos = [self.pos.row, self.pos.col]

    def moveTowards(self, playerPos):
        # Update internal position for movement logic
        newPos = self.move_towards_player([playerPos.row, playerPos.col])
        self.pos.row = newPos[0]
        self.pos.col = newPos[1]

def train(player, monster, goal):
    actionMap = {UP: player.moveUp, DOWN: player.moveDown, LEFT: player.moveLeft, RIGHT: player.moveRight}
    qtable = generateQtable(GRID_SIZE)
    esp = EPSILON
    goalPos = Point(goal[0], goal[1])

    for episole in range(EPISOLES):
        gameOver = False
        player.reset()
        monster.reset()
        currentState = coorTuplesToId(player.pos.toTuple(), monster.pos.toTuple())

        timestep = 0
        path = []
        found = False
        # start a run
        while not gameOver:
            rand = random.random()
            actionStrat = EXPLORE if rand < esp else EXPLOIT
            chosenAction = None

            validMoves = player.findValidMoves()
            if actionStrat == EXPLORE:
                randIndex = random.randint(0, len(validMoves) - 1)
                chosenAction = validMoves[randIndex]
            else:
                stateScores = qtable[currentState]
                chosenAction = validMoves[0]
                highestScore = stateScores[chosenAction]
                for action in validMoves:
                    score = stateScores[action]
                    if score > highestScore:
                        highestScore = score
                        chosenAction = action

            monsterDis1 = getDistance(player.pos, monster.pos)
            goalDis1 = getDistance(player.pos, goalPos)

            actionFunc = actionMap[chosenAction]
            actionFunc()
            monster.moveTowards(player.pos)

            monsterDis2 = getDistance(player.pos, monster.pos)
            goalDis2 = getDistance(player.pos, goalPos)

            point = getReward(player.pos, goalPos, monster.pos, (goalDis1, goalDis2), (monsterDis1, monsterDis2), path)
            if point == LOOSE_SCORE or point == WIN_SCORE:
                gameOver = True
            if point == WIN_SCORE:
                found = True

            nextStateScores = qtable[coorTuplesToId(player.pos.toTuple(), monster.pos.toTuple())]
            nextHighestScore = nextStateScores[0]
            for score in nextStateScores:
                if score > nextHighestScore:
                    nextHighestScore = score

            # UPDATE QTABLE ENTRY
            qtable[currentState][chosenAction] = qtable[currentState][chosenAction] + ALPHA * (point + GAMMA * nextHighestScore - qtable[currentState][chosenAction])

            currentState = coorTuplesToId(player.pos.toTuple(), monster.pos.toTuple())
            timestep += 1
        
        
        if esp > EPS_MIN:
            esp = esp * EPS_DECAY
        # else:
        #     break
    print("Solution found: ", found)

    print("✅ Training complete.")
    return qtable


def train_all_levels():
    level_manager = LevelManager()
    for level_index in range(1, 9):
        print(f"\n🔁 Training level {level_index}...")
        level_manager.current_level = level_index
        level_data = level_manager.get_level_data()

        walls = level_data["walls"]

        player_pos = level_data["player_pos"]
        monster_pos = level_data["mummy_pos_white"]
        goal_pos = level_data["stair_pos"]

        player = BotAdapter(player_pos, GRID_SIZE, walls)
        monster = EnemyAdapter(monster_pos, GRID_SIZE, walls)

        qtable = train(player, monster, goal_pos)
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