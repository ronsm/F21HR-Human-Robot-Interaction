from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio
import cozmo

"""
CLASS: search.py

Controls the search operations taking place in Step 1.
"""
class Search(object):
    def __init__(self, robot: cozmo.robot.Robot, pos):
        print('[SEARCH] I am the search controller.')

        self.robot = robot
        self.currentPos = pos
        self.nextPos = [1, 1, 0]

    """
    Author: Ronnie Smith
    
    Follows a path around the map to search for the object.
    """
    async def search(self):

        # Path to follow - robot will not make it through all of them in the scenario
        # as it should find the cube before then. Path currently does not cover whole arena,
        # since robot 1 might collide with robot 2.
        actions = ["down", "down", "left", "down", "down", "left", "left", "up", "up", "right", "right", "right", "right", "down", "down", "down"]

        # For every spot landed on after an action, execute a search-on-spot
        found = False
        for i in range(len(actions)):
            print('Moving: ', actions[i])
            await self.move(actions[i])
            found = await self.searchOnSpot()
            if found == True:
                break

        print('Cube detected whilst robot at position x:', self.currentPos[0], 'y:', self.currentPos[1])

        return found, self.currentPos

    """
    Author: Ronnie Smith
    
    Turns the robot on the spot to search for a cube in each direction along the map.
    """
    async def searchOnSpot(self):
        found = False

        # Look down 0, 90, 180, 270 angles when on the spot, to see if cube is in adject grid positions
        for i in range(0, 4):
            await self.robot.turn_in_place(degrees(90), in_parallel=False, num_retries=0, speed=degrees(45), accel=None, angle_tolerance=degrees(2), is_absolute=False).wait_for_completed()
            cube = None

            # This is a small odometry correction as the robot tends to drift during the spinning
            if i == 2:
                await self.robot.drive_straight(distance_mm(-15), speed_mmps(50)).wait_for_completed()

            # Check for an observable light cube
            try:
                cube = await self.robot.world.wait_for_observed_light_cube(timeout=2)
                print("Object found!", cube)

            except asyncio.TimeoutError:
                print('No object detected.')

            if cube != None:
                found = True
                break

        return found

    """
    Author: Ronnie Smith
    
    Moves the robot and saves the new position.

    NOTE: This is a duplicate of a function in astart.py, there were some
    issues trying to run it from the other class.
    """
    async def move(self, direction):
        success = 0

        # Modifies the current position based on the move action given
        # Uses the face function to make sure robot is facing correct direction before
        # attempting to move it forward
        if direction == "up":
            self.nextPos[1] = self.currentPos[1] - 2
            await self.face("north")
            success = 1
        elif direction == "down":
            self.nextPos[1] = self.currentPos[1] + 2
            await self.face("south")
            success = 1
        elif direction == "left":
            self.nextPos[0] = self.currentPos[0] + 2
            await self.face("west")
            success = 1
        elif direction == "right":
            self.nextPos[0] = self.currentPos[0] + 2
            await self.face("east")
            success = 1
        else:
            print('[GRID] Unable to execute navigation command: invalid direction provided.')

        #self.currentPos = self.nextPos
        self.currentPos[0] = self.nextPos[0]
        self.currentPos[1] = self.nextPos[1]

        # Move the robot forward if the robot succesfully faced the right way
        if success == 0:
            print('[GRID] Unable to execute navigation command: new grid position occupied.')
        elif success == 1:
            await self.robot.drive_straight(distance_mm(250), speed_mmps(50)).wait_for_completed()
            
    """
    Author: Ronnie Smith
    
    Turns the robot to face a given direction, based on current heading.

    NOTE: This is a duplicate of a function in astart.py, there were some
    issues trying to run it from the other class.
    """
    async def face(self, direction):
        currentHeading = self.currentPos[2]

        # Make a turn based on the current heading
        # Adjust current heading to match command
        if direction == "north":
            if currentHeading == 270:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 0) * -1.0
            self.currentPos[2] = 0
        elif direction == "south":
            if currentHeading == 90:
                headingDifference = -90
            else:
                headingDifference = (currentHeading - 180) * -1.0
            self.currentPos[2] = 180
        elif direction == "east":
            if currentHeading == 180:
                headingDifference = 90
            else:
                headingDifference = (currentHeading - 90) * -1.0
            self.currentPos[2] = 90
        elif direction == "west":
            if currentHeading == 0:
                headingDifference = 90
            else:
                headingDifference = (currentHeading - 270) * -1.0
            self.currentPos[2] = 270
        else:
            print("[GRID] Invalid direction given to face(self, direction)")

        print('Turning', headingDifference, 'to face', direction)
        await self.robot.turn_in_place(degrees(headingDifference), in_parallel=False, num_retries=0, speed=degrees(45), accel=None, angle_tolerance=degrees(2), is_absolute=False).wait_for_completed()