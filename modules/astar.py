from __future__ import print_function
import heapq
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
import cozmo

"""

The A* algorithm here is based on the one implemented by Lauren Luce. Functions that do not have an author indicated should
be assumed to have originated from the source below.
Source: https://github.com/laurentluce/python-algorithms/tree/master/algorithms/

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
    def __init__(self, robot: cozmo.robot.Robot, pos):
        self.opened = []
        heapq.heapify(self.opened)

        self.currentPos = pos
        self.nextPos = [1, 1, 0]

        self.robot = robot

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
        # walls = ((0, 5), (1, 1), (1, 3), (1, 5), (1, 7), (2, 7), (3, 1), (3, 3), (3, 5), (3, 6), (3, 7), (4, 3),
        #         (5, 1), (5, 2), (5, 3), (5, 5), (5, 7), (5, 8), (6, 1), (6, 2), (6, 3), (6, 7), (6, 8), (7, 1),
        #         (7, 2), (7, 3), (7, 4), (7, 5), (7, 7), (7, 8), (8, 7), (8, 8))

        walls = ((0, 0), (0, 1), (0, 7), (0, 8), (1, 0), (1, 1), (1, 3), (1, 5), (1, 7), (1, 8), (2, 3), (2, 7), (2, 8), 
                (3, 1), (3, 3), (3, 4), (3, 5), (3, 7), (3, 8), (5, 1), (5, 3), (5, 5), (5, 6), (5, 7), (6, 1), (7, 1),
                (7, 2), (7, 3), (7, 5), (7, 6), (7, 7), (6, 2))

        self.init_grid(9, 9, walls, start, end)

        path = self.solve()
        actions = self.pathToActions(path)
        return actions

    """
    Author: Ronnie Smith
    
    Converts the A* path to a list of actions that can be executed by the Grid handler to move Cozmo.
    """
    def pathToActions(self, path):
        newPath = []
        j = 0
        for i in range(len(path)):
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
        print(self.currentPos)
        print('Actions:', actions)
        self.printPath(path)

        return actions

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

    """
    Author: Ronnie Smith
    
    Moves the robot and saves the new position.
    """
    async def move(self, direction):
        success = 0

        yMod = False
        xMod = False

        if direction == "up":
            self.nextPos[0] = self.currentPos[0] - 2
            await self.face("north")
            success = 1
            yMod = True
        elif direction == "down":
            self.nextPos[0] = self.currentPos[0] + 2
            await self.face("south")
            success = 1
            yMod = True
        elif direction == "left":
            self.nextPos[1] = self.currentPos[1] - 2
            await self.face("west")
            success = 1
            xMod = True
        elif direction == "right":
            self.nextPos[1] = self.currentPos[1] + 2
            await self.face("east")
            success = 1
            xMod = True
        else:
            print('[GRID] Unable to execute navigation command: invalid direction provided.')

        #self.currentPos = self.nextPos
        if yMod == True:
            self.currentPos[0] = self.nextPos[0]
        if xMod == True:
            self.currentPos[1] = self.nextPos[1]

        if success == 0:
            print('[GRID] Unable to execute navigation command: new grid position occupied.')
        elif success == 1:
            await self.robot.drive_straight(distance_mm(250), speed_mmps(50)).wait_for_completed()

    """
    Author: N/A
    
    Turns the robot and adjusts the stored rotation.
    """
    async def turn(self, rotation):
        self.nextPos[2] = self.currentPos[2] + rotation

        await self.robot.turn_in_place(rotation).wait_for_completed()

        self.currentPos = self.nextPos

    """
    Author: Ronnie Smith
    
    Turns the robot to face a given direction, based on current heading.
    """
    async def face(self, direction):
        currentHeading = self.currentPos[2]

        if direction == "north":
            if currentHeading == 270:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 0) * 1.0
            self.currentPos[2] = 0
        elif direction == "south":
            if currentHeading == 90:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 180) * 1.0
            self.currentPos[2] = 180
        elif direction == "east":
            if currentHeading == 180:
                headingDifference = 90
            elif currentHeading == 0:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 90) * -1.0
            self.currentPos[2] = 90
        elif direction == "west":
            if currentHeading == 0:
                headingDifference = 90
            elif currentHeading == 180:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 270) * -1.0
            self.currentPos[2] = 270
        else:
            print("[GRID] Invalid direction given to face(self, direction)")

        print('Turning', headingDifference, 'to face', direction)
        await self.robot.turn_in_place(degrees(headingDifference), in_parallel=False, num_retries=3, speed=degrees(70), accel=None, angle_tolerance=degrees(2), is_absolute=False).wait_for_completed()

    """
    Author: Ronnie Smith
    
    Returns current position of robot.
    """
    def getPos(self):
        pos = self.currentPos
        return pos