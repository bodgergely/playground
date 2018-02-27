from maze import Maze
import numpy as np

PLAYER_ID = 5
PLAYER_CHAR = 'P'

ENEMY_ID = 7
ENEMY_CHAR = 'E'


class Dungeon:
    def __init__(self, maze):
        self.maze = maze
        self.enemy_to_pos = dict()
        self.position_to_enemy = dict()
    def add_player(self, player):
        self.player = player
        self._place_agent(self.player, self._random_pos(), PLAYER_ID, PLAYER_CHAR)

    def add_enemy(self, enemy):
        self._place_agent(enemy, self._random_pos(), ENEMY_ID, ENEMY_CHAR)
        self.position_to_enemy[enemy.get_position()] = enemy
        self.enemy_to_pos[enemy] = enemy.get_position()

    def display(self):
        return str(self.maze)

    def _random_pos(self):
        tries = 0
        while True:
            tries+=1
            r = np.random.randint(1, self.maze.size) 
            c = np.random.randint(1, self.maze.size)
            if self.maze.is_free((r,c)):
                return r,c
            elif tries >= 1000:
                raise Exception(f'Can not seem to get free position on maze after {tries} attempts!')


    def _place_agent(self, agent, pos, ID, character):
        if agent.get_position():
            self.maze.free_field(agent.get_position())
        agent.set_position(pos)
        self.maze.reserve_field(pos, ID, character)
                

class Agent:
    def __init__(self):
        self.pos = None
    def get_position(self):
        return self.pos
    def set_position(self, pos):
        self.pos = pos


class Enemy(Agent):
    def __init__(self):
        super().__init__()

class Player(Agent):
    def __init__(self):
        super().__init__()



if __name__ == "__main__":
    maze = Maze(20)
    dungeon = Dungeon(maze)
    player = Player()
    enemy = Enemy()
    dungeon.add_player(player)
    dungeon.add_enemy(enemy)
    print(dungeon.display())

