import grid
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):

    myGrid = grid.Grid(robot)

    myGrid.startLocalisation()

    myGrid.printGrid()

    # TEST CODE START HERE

    myGrid.move("down")
    myGrid.printGrid()
    myGrid.move("right")

    # TEST CODE END HERE
    
    myGrid.printGrid()

cozmo.run_program(cozmo_program)