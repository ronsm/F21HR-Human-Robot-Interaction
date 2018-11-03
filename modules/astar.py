from __future__ import print_function
import heapq

"""

The A* algorithm here is based on the one implemented by Lauren Luce. Unless otherwise stated, functions in the AStar class are hers.
Source: https://github.com/laurentluce/python-algorithms/tree/master/algorithms/tests

"""
class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)

        self.closed = set()

        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)

            self.closed.add(cell)

            if cell is self.end:
                return self.get_path()

            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

    """
    Author: Ronnie Smith
    
    Prints the grid occupancy map.
    """
    def printGrid(self):
        print('')
        print('[LEGO WORLD]')
        for i in range(0, len(self.cells)):
            if self.cells[i].reachable == True:
                print('[0]', end='')
            else:
                print('[1]', end='')
            if (i % self.grid_width) == self.grid_width - 1 and i != 0:
                print('')
        print('')

    """
    Author: Ronnie Smith
    
    Initialises the lego world by setting obstacle/wall positions.
    """

    def initLegoWorld(self, start, end):
        walls = ((0, 5), (1, 1), (1, 3), (1, 5), (1, 7), (2, 7), (3, 1), (3, 3), (3, 5), (3, 6), (3, 7), (4, 3),
                (5, 1), (5, 2), (5, 3), (5, 5), (5, 7), (5, 8), (6, 1), (6, 2), (6, 3), (6, 7), (6, 8), (7, 1),
                (7, 2), (7, 3), (7, 4), (7, 5), (7, 7), (7, 8), (8, 7), (8, 8))
        self.init_grid(9, 9, walls, start, end)

        path = self.solve()
        self.pathToActions(path)

    """
    Author: Ronnie Smith
    
    Converts the A* path to a list of actions that can be executed by the Grid handler to move Cozmo.
    """
    def pathToActions(self, path):
        newPath = []
        j = 0
        for i in range(0, len(path)):
            if i % 2 == 0:
                newPath.append(path[i])
                j = j + 1

        actions = []
        for i in range(1, len(newPath)):
            if newPath[i][0] > newPath[i - 1][0]:
                actions.append("down")
            elif newPath[i][0] < newPath[i - 1][0]:
                actions.append("up")
            elif newPath[i][1] > newPath[i - 1][1]:
                actions.append("right")
            elif newPath[i][1] < newPath[i - 1][1]:
                actions.append("left")
            elif newPath[i][0] == newPath[i - 1][0] and newPath[i][1] == newPath[i - 1][1]:
                print('[A*] Cannot move to same position.')
            else:
                print('[A*] Cannot move diagonally.')

        print('Full path:', path)
        print('Action path:', newPath)
        print('Actions:', actions)
        self.printPath(path)

    """
    Author: Ronnie Smith
    
    Prints the path generated by the A* algorithm.
    """
    def printPath(self, path):
        print('')
        print('[LEGO WORLD]')
        for i in range(0, len(self.cells)):
            res = self.cellIsOnPath(path, self.cells[i].x, self.cells[i].y)
            if res == True:
                print('[*]', end='')
            else:
                if self.cells[i].reachable == True:
                    print('[0]', end='')
                elif self.cells[i].reachable == False:
                    print('[1]', end='')

            if (i % self.grid_width) == self.grid_width - 1 and i != 0:
                print('')
        print('')

    """
    Author: Ronnie Smith
    
    Checks if a cell in the grid is part of a given path generated by the A* algorithm.
    """
    def cellIsOnPath(self, path, x, y):
        isOnPath = False

        for i in range(0, len(path)):
            if path[i][0] == x and path[i][1] == y:
                isOnPath = True

        return isOnPath

print('Navigating from:', (0, 0), 'to', (6, 4))
print('')
a = AStar()
a.initLegoWorld((0, 0), (6, 4))