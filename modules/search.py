from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio
import cozmo

class Search(object):
    def __init__(self, robot: cozmo.robot.Robot, pos):
        print('[SEARCH] I am the search controller.')

        self.robot = robot
        self.currentPos = pos
        self.nextPos = [1, 1, 0]

    def search(self):
        actions = ["down", "down", "left", "down", "down", "right", "right", "up"]

        found = False
        for i in range(len(actions)):
            self.move(actions[i])
            found = self.searchOnSpot()
            if found == True:
                break

        print('Cube detected whilst robot at position x:', self.currentPos[0], 'y:', self.currentPos[1])

        return found, self.currentPos

    def searchOnSpot(self):
        found = False
        for i in range(0, 4):
            self.robot.turn_in_place(degrees(90)).wait_for_completed()

            cube = None

            try:
                cube = self.robot.world.wait_for_observed_light_cube(timeout=2)
                print("Object found!", cube)

            except asyncio.TimeoutError:
                print('No object detected.')

            if cube != None:
                found = True
                break

        return found

    def move(self, direction):
        success = 0

        if direction == "up":
            self.nextPos[1] = self.currentPos[1] - 2
            self.face("north")
            success = 1
        elif direction == "down":
            self.nextPos[1] = self.currentPos[1] + 2
            self.face("south")
            success = 1
        elif direction == "left":
            self.nextPos[0] = self.currentPos[0] + 2
            self.face("west")
            success = 1
        elif direction == "right":
            self.nextPos[0] = self.currentPos[0] + 2
            self.face("east")
            success = 1
        else:
            print('[GRID] Unable to execute navigation command: invalid direction provided.')

        #self.currentPos = self.nextPos
        self.currentPos[0] = self.nextPos[0]
        self.currentPos[1] = self.nextPos[1]

        if success == 0:
            print('[GRID] Unable to execute navigation command: new grid position occupied.')
        elif success == 1:
            self.robot.drive_straight(distance_mm(250), speed_mmps(50)).wait_for_completed()

    def face(self, direction):
        currentHeading = self.currentPos[2]

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
        self.robot.turn_in_place(degrees(headingDifference)).wait_for_completed()