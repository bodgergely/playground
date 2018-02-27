import numpy as np
from random import shuffle

def generate_maze(maze):
       
    def adjacent(maze, prev, r, c, debug=''):
        h, w = maze.shape
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                nr = r + i
                nc = c + j
                if (i == 0 and j == 0) or (nr == prev[0] and nc == prev[1]) or (nc == prev[0] and nr == prev[1]):
                    continue
                if nr < 0 or nr >= h or nc < 0 or nc >= w:
                    return True
                if maze[nr, nc] == 0:
                    if debug == 'up':
                        print("up:", prev, r, c, nr, nc)
                    return True
        return False

    def left(maze, pos):
        r, c = pos[0], pos[1] - 1
        if c <= 0 or maze[r,c] == 0 or adjacent(maze, pos, r, c):
            return None
        else:
            return r,c
    def right(maze, pos):
        r, c = pos[0], pos[1] + 1
        if c >= maze.shape[1]-1 or maze[r,c] == 0 or adjacent(maze, pos ,r, c):
            return None
        else:
            return r,c

    def up(maze, pos):
        r, c = pos[0] - 1, pos[1]
        if r <= 0 or maze[r,c] == 0 or adjacent(maze, pos, r, c, debug='up'):
            return None
        else:
            return r,c
    def down(maze, pos):
        r, c = pos[0] + 1, pos[1]
        if r >= maze.shape[0]-1 or maze[r,c] == 0 or adjacent(maze, pos ,r, c):
            return None
        else:
            return r,c


    def neighbors(maze, curr_pos):
        h, w = maze.shape
        nbs = []
        functions = [left, right, up, down]
        return list(filter(lambda x : x!=None,  [f(maze, curr_pos) for f in functions]))


    def generate(maze, curr_pos):
        maze[curr_pos] = 0
        print(str(maze))
        nbs = neighbors(maze, curr_pos)
        if not nbs:
            return
        shuffle(nbs)
        print("neigbors: ", nbs)
        for nb in nbs:
            generate(maze, nb)
            print('at: ', nb)

    height, width = maze.shape
    r = np.random.randint(1, height-1)
    c = 0
    start = r, c
    generate(maze, start)



class Maze:
    def __init__(self, size):
        self.maze = np.ones((size,size))
        generate_maze(self.maze)
    def __str__(self):
        return str(self.maze)


m = Maze(10)
print(m)
