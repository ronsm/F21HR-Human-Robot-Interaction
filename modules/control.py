from astar import AStar
from search import Search
from interact import Interact
from comms import Comms
import cozmo
import asyncio
import sys
from cozmo.util import degrees, distance_mm, speed_mmps

async def cozmo_program(sdk_conn1, sdk_conn2):

    robot1 = await sdk_conn1.wait_for_robot()
    robot2 = await sdk_conn2.wait_for_robot()

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

    # Step 3]
    currentPos = [6, 4, 90] # USE ONLY IF PREVIOUS STEP IS DISABLED
    await step_3(robot1, robot2, currentPos)

    # Step 4
    # currentPos = [4, 6, 0] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, currentPos = step_4(robot, currentPos)
    # if res == False:
    #     print('[ERROR][STEP 4] Unable to move Robot 1 to observation position.')
    # print(currentPos)

    # Step 5

    # Step 6

    # Step 7
    # step_7(robot)
    

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
async def step_3(robot1, robot2, currentPos):
    comms1 = Comms(robot1)
    comms2 = Comms(robot2)
    await comms1.load()
    await comms2.load()

    y = currentPos[0]
    x = currentPos[1]

    if y == 0:
        y = 0
    elif y == 2:
        y = 1
    elif y == 4:
        y = 2
    elif y == 6:
        y = 3
    elif y == 8:
      y = 4

    if x == 0:
        x = 0
    elif x == 2:
        x = 1
    elif x == 4:
        x = 2
    elif x == 6:
        x = 3
    elif x == 8:
      x = 4

    comms1.display(y)
    res = await comms2.read()
    comms1.clear(1)

    if res == -1:
        print('[ERROR][CONTROL] Robot 2 was unable to detect Robot 1 coordinate Y. ')
    
    await asyncio.sleep(2)

    comms1.display(x)
    res = await comms2.read()
    comms1.clear(1)

    if res == -1:
        print('[ERROR][CONTROL] Robot 2 was unable to detect Robot 1 coordinate X. ')

    await asyncio.sleep(1)

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

#cozmo.run_program(cozmo_program, use_viewer=True)

if __name__ == '__main__':
    cozmo.setup_basic_logging()
    loop = asyncio.get_event_loop()

    try:
        conn1 = cozmo.connect_on_loop(loop)
        conn2 = cozmo.connect_on_loop(loop)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)

    #cozmo.run_program(cozmo_program(conn1, conn2), use_viewer=True)

    # Run a coroutine controlling both connections
    loop.run_until_complete(cozmo_program(conn1, conn2))