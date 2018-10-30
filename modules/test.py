import grid
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

grid = grid.Grid(cozmo.robot.Robot)
robot = cozmo.robot.Robot

def cozmo_program(robot: cozmo.robot.Robot):

    grid.startLocalisation()

    # TEST CODE START HERE

    robot.turn_in_place(degrees(90)).wait_for_completed()

    grid.move("down")

    # TEST CODE END HERE
    
    grid.printGrid()

cozmo.run_program(cozmo_program)