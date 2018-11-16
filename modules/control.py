from astar import AStar
from search import Search
from interact import Interact
from comms import Comms
import cozmo
import numpy as np
import asyncio
import sys
from cozmo.util import degrees, distance_mm, speed_mmps

async def cozmo_program(sdk_conn1, sdk_conn2):

    robot1 = await sdk_conn1.wait_for_robot()
    robot2 = await sdk_conn2.wait_for_robot()

    # We will check whether each step is successful
    res = False

    # currentPos1 = [0, 3, 180] # Initialised at Step 1
    # currentPos2 = [2, 6, 180] # Initialised at Step 2

    # Step 1
    # res, currentPos1 = await step_1(robot1, currentPos1) # currentPos = [3, 2, 90]
    # destPos = currentPos1
    # if res == False:
    #     print('[ERROR][STEP 1] Could not find cube on search path.')

    # Step 2
    # currentPos1 = [6, 4, 90] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, currentPos1 = await step_2(robot1, currentPos1)
    # if res == False:
    #     print('[ERROR][STEP 2] Unable to move Robot 1 to face Robot 2.')
    # print(currentPos1)

    # Step 3]
    # destPos = [6, 4, 90]     # USE ONLY IF PREVIOUS STEP IS DISABLED
    # currentPos1 = [6, 4, 90] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, destPos = await step_3(robot1, robot2, destPos)
    # if res == False:
    #     print('[ERROR][STEP 3] Robot syncronisation process failed.')

    # # Step 4
    # currentPos1 = [4, 6, 0] # USE ONLY IF PREVIOUS STEP IS DISABLED
    # res, currentPos1, currentPos2 = await step_4(robot1, robot2, currentPos1, currentPos2, destPos)
    # if res == False:
    #     print('[ERROR][STEP 4] Unable to move Robot 1 to observation position.')
    # print(currentPos1, currentPos2)

    # Step 5
    # await step_5(robot1)

    # Step 6
    currentPos1 = [8, 4, 0]  # USE ONLY IF PREVIOUS STEP IS DISABLED
    currentPos2 = [6, 4, 90] # USE ONLY IF PREVIOUS STEP IS DISABLED
    res, currentPos1, currentPos2 = await step_6(robot1, robot2, currentPos1, currentPos2)

    # Step 7
    # await step_7(robot1)
    

# ROBOT 1 finds the cube
async def step_1(robot1, currentPos1):
    s = Search(robot1, currentPos1)
    found, currentPos1 = await s.search()
    
    if found == True:
        return True, currentPos1
    else:
        return False, currentPos1

# ROBOT 1 returns to face ROBOT 2
async def step_2(robot1, currentPos1):
    a = AStar(robot1, currentPos1)

    print('Navigating from:', (6, 4), 'to', (4, 6))
    print('')
    
    path = a.initLegoWorld((6, 4), (4, 6))
    for i in range(len(path)):
        await a.move(path[i])

    await a.face("north")
    currentPos = a.getPos()

    return True, currentPos

# ROBOT 1 and ROBOT 2 engage in position information transfer
async def step_3(robot1, robot2, destPos):
    res = False

    comms1 = Comms(robot1)
    comms2 = Comms(robot2)
    await comms1.load()
    await comms2.load()

    y = destPos[0]
    x = destPos[1]

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

    destPos = [0, 0]

    print('y', y, 'x', x)

    comms1.display(y)
    res = await comms2.read()
    destPos[0] = res
    comms1.clear()

    if res == -1:
        print('[ERROR][CONTROL] Robot 2 was unable to detect Robot 1 coordinate Y. ')
    
    await asyncio.sleep(2)

    comms1.display(x)
    res = await comms2.read()
    destPos[1] = res
    comms1.clear()

    if res == -1:
        print('[ERROR][CONTROL] Robot 2 was unable to detect Robot 1 coordinate X. ')

    await asyncio.sleep(2)

    return True, destPos

# ROBOT 1 and ROBOT 2 navigate to:
#    + ROBOT 1: position to watch robot 2 pick up the cube
#    + ROBOT 2: position to pick up the cube
async def step_4(robot1, robot2, currentPos1, currentPos2, destPos):
    # ROBOT 1
    a = AStar(robot1, currentPos1)

    print('Navigating from:', (4, 6), 'to', (8, 4))
    print('')
    
    path = a.initLegoWorld((4, 6), (8, 4))
    for i in range(len(path)):
        await a.move(path[i])

    await a.face("north")
    currentPos1 = a.getPos()

    # ROBOT 2
    a = AStar(robot2, currentPos2)

    print('Navigating from:', (2, 6), 'to', (6, 4))
    print('')
    
    dest = (destPos[0], destPos[1])

    path = a.initLegoWorld((2, 6), dest)
    for i in range(len(path)):
        await a.move(path[i])

    await a.face("east")
    currentPos1 = a.getPos()

    return True, currentPos1, currentPos2

# ROBOT 2 picks up the cube
async def step_5(robot2):
    interact = Interact(robot2)

    initialPose = [robot2.pose.position.x, robot2.pose.position.y]
    print(initialPose)
    
    res = await interact.pickupCube()

    finalPose = [robot2.pose.position.x, robot2.pose.position.y]
    print(finalPose)

    b = finalPose[0] - initialPose[0]
    a = finalPose[1] - initialPose[1]
    hyp = np.sqrt(b**2 - a**2)

    await asyncio.sleep(1)

    await robot2.drive_straight(distance_mm(-hyp), speed_mmps(50)).wait_for_completed()

    print(hyp)

# ROBOT 2 brings the cube to place on map where person can be seen
# ROBOT 1 follows ROBOT 2 after a pause
async def step_6(robot1, robot2, currentPos1, currentPos2):
    # ROBOT 2
    a = AStar(robot2, currentPos2)

    print('Navigating from:', (6, 4), 'to', (4, 0))
    print('')

    path = a.initLegoWorld((6, 4), (4, 0))
    for i in range(len(path)):
        await a.move(path[i])

    await a.face("south")
    currentPos2 = a.getPos()


    # ROBOT 1
    a = AStar(robot1, currentPos1)

    print('Navigating from:', (8, 4), 'to', (4, 2))
    print('')
    
    path = a.initLegoWorld((8, 4), (4, 2))
    for i in range(len(path)):
        await a.move(path[i])

    currentPos1 = a.getPos()

    await robot1.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
    await robot1.turn_in_place(degrees(50)).wait_for_completed()

    return True, currentPos1, currentPos2

# ROBOT 2 puts down the cube
# ROBOT 2 then searches for person
async def step_7(robot1):
    interact = Interact(robot1)
    res = await interact.detectPerson()

    if res == True:
        print('Found a face')

if __name__ == '__main__':
    cozmo.setup_basic_logging()
    loop = asyncio.get_event_loop()

    try:
        conn1 = cozmo.connect_on_loop(loop)
        conn2 = cozmo.connect_on_loop(loop)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)

    # Run a coroutine controlling both connections
    loop.run_until_complete(cozmo_program(conn1, conn2))