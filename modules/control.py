from astar import AStar
from search import Search
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):

    step_1(robot)

# ROBOT 1 finds the cube
def step_1(robot):
    currentPos = [0, 1, 180]
    s = Search(robot, currentPos)
    found = s.search()

# ROBOT 1 returns to face ROBOT 2
def step_2(robot):
    pass

# ROBOT 1 and ROBOT 2 engage in position information transfer
def step_3(robot):
    pass

# ROBOT 1 and ROBOT 2 navigate to:
#    + ROBOT 1: position to watch robot 2 pick up the cube
#    + ROBOT 2: position to pick up the cube
def step_4(robot):
    currentPos = [0, 0, 180]
    a = AStar(robot, currentPos)

    print('Navigating from:', (0, 0), 'to', (2, 2))
    print('')
    
    path = a.initLegoWorld((0, 0), (2, 2))
    for i in range(len(path)):
        a.move(path[i])

    currentPos = a.getPos()
    a = AStar(robot, currentPos)

    print('')
    print('Navigating from:', (2, 2), 'to', (0, 0))
    print('')

    path = a.initLegoWorld((2, 2), (0, 0))
    for i in range(len(path)):
        a.move(path[i])

cozmo.run_program(cozmo_program)