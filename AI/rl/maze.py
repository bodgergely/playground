import numpy as np
from random import shuffle
from collections import deque

def generate_maze(maze):
    
    def corner_case(maze, r, c, from_r, from_c):
        if maze[r,c] == 0:
            if (maze[r, c-1] == 1 and maze[r+1, c] == 1) or (maze[r, c-1] == 1 and maze[r-1, c] == 1) or (maze[r, c+1] == 1 and maze[r-1, c] == 1) or (maze[r, c+1] == 1 and maze[r+1, c] == 1):
                return True
        return False

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
                    if (i in (-1, 1) and j == 0) or (j in (-1,1) and i==0) and maze[nr,nc] == 0:
                        return True
                    elif corner_case(maze, nr, nc, r, c):
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
        functions = shuffle([left, right, up, down])
        for f in functions:
            yield f(maze, curr_pos)


    
    def generate_recursive(maze, curr_pos):
        maze[curr_pos] = 0
        functions = [left, right, up, down]
        shuffle(functions)
        for f in functions:
            nb = f(maze, curr_pos)
            if not nb:
                continue
            generate(maze, nb)
    

    def generate(maze, curr_pos):
        stack = deque()
        functions = [left, right, up, down]
        shuffle(functions)
        maze[curr_pos] = 0
        for f in functions:
            stack.append((f, curr_pos))
        while len(stack) > 0:
            f, curr_pos = stack.pop()
            nb = f(maze, curr_pos)
            if nb != None:
                maze[nb] = 0
                shuffle(functions)
                for f in functions:
                    stack.append((f, nb))

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
        r,c = self.maze.shape
        rep = ""
        for i in range(r):
            for j in range(c):
                rep += str(int(self.maze[i,j])) + " "
            rep += '\n'
        return rep


m = Maze(50)
print(m)
