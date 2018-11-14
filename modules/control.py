from astar import AStar
from search import Search
from interact import Interact
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):

    # We will check whether each step is successful
    res = False

    # Step 1
    # currentPos = [0, 3, 180]
    # res, currentPos = step_1(robot, currentPos) # currentPos = [3, 2, 90]
    # if res == False:
    #     print('[ERROR][STEP 1] Could not find cube on search path.')

    # Step 2
    # currentPos = [6, 4, 90] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, currentPos = step_2(robot, currentPos)
    # if res == False:
    #     print('[ERROR][STEP 2] Unable to move Robot 1 to face Robot 2.')
    # print(currentPos)

    # Step 3

    # Step 4
    # currentPos = [4, 6, 0] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, currentPos = step_4(robot, currentPos)
    # if res == False:
    #     print('[ERROR][STEP 4] Unable to move Robot 1 to observation position.')
    # print(currentPos)

    # Step 5

    # Step 6

    # Step 7
    step_7(robot)
    

# ROBOT 1 finds the cube
def step_1(robot, currentPos):
    s = Search(robot, currentPos)
    found, currentPos = s.search()
    
    if found == True:
        return True, currentPos
    else:
        return False, currentPos

# ROBOT 1 returns to face ROBOT 2
def step_2(robot, currentPos):
    a = AStar(robot, currentPos)

    print('Navigating from:', (6, 4), 'to', (4, 6))
    print('')
    
    path = a.initLegoWorld((6, 4), (4, 6))
    for i in range(len(path)):
        a.move(path[i])

    a.face("north")
    currentPos = a.getPos()

    return True, currentPos

# ROBOT 1 and ROBOT 2 engage in position information transfer
def step_3(robot):
    pass

# ROBOT 1 and ROBOT 2 navigate to:
#    + ROBOT 1: position to watch robot 2 pick up the cube
#    + ROBOT 2: position to pick up the cube
def step_4(robot, currentPos):
    a = AStar(robot, currentPos)

    print('Navigating from:', (4, 6), 'to', (8, 5))
    print('')
    
    path = a.initLegoWorld((4, 6), (8, 4))
    for i in range(len(path)):
        a.move(path[i])

    a.face("north")
    currentPos = a.getPos()

    return True, currentPos
    # a = AStar(robot, currentPos)

    # print('')
    # print('Navigating from:', (2, 2), 'to', (0, 0))
    # print('')

    # path = a.initLegoWorld((2, 2), (0, 0))
    # for i in range(len(path)):
    #     a.move(path[i])

# ROBOT 2 picks up the cube
def step_5(robot, currentPos):
    pass

# ROBOT 2 brings the cube to place on map where person can be seen
# ROBOT 1 follows ROBOT 2 after a pause
def step_6(robot, currentPos):
    pass

# ROBOT 2 puts down the cube
# ROBOT 2 then searches for person
def step_7(robot):
    interact = Interact(robot)
    interact.detectPerson()

cozmo.run_program(cozmo_program, use_viewer=True)