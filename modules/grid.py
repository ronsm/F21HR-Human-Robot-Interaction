#!/usr/bin/env python3

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import math
import numpy as np

class Grid:
    def __init__(self, robot: cozmo.robot.Robot):
        self.gridSmall = [[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 1],
                        [0, 0, 0, 0, 1]]

        self.gridLarge = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                          [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                          [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                          [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.currentPos = [1, 1, 0]
        self.nextPos = [1, 1, 0]

        self.robot = robot

    def printGrid(self):
        print('GRID')
        for i in range(0, len(self.gridLarge)):
            print(self.gridLarge[i])
        print('')

    def startLocalisation(self):
        self.locGrid = self.gridLarge

        self.locGrid[1][1] = 2
        self.currentPos[0] = 1
        self.currentPos[1] = 1

    def move(self, direction):
        self.clearRobotPos()
        success = 0

        if direction == "up":
            if self.locGrid[self.currentPos[0]][self.currentPos[1]-1] == 0:
                self.nextPos[1] = self.currentPos[1] - 2
                self.face("north")
                success = 1
        elif direction == "down":
            if self.locGrid[self.currentPos[0]][self.currentPos[1]+1] == 0:
                self.nextPos[1] = self.currentPos[1] + 2
                self.face("south")
                success = 1
        elif direction == "left":
            if self.locGrid[self.currentPos[0]-1][self.currentPos[1]] == 0:
                self.nextPos[0] = self.currentPos[0] + 2
                self.face("west")
                success = 1
        elif direction == "right":
            if self.locGrid[self.currentPos[0]+1][self.currentPos[1]] == 0:
                self.nextPos[0] = self.currentPos[0] + 2
                self.face("east")
                success = 1
        else:
            print('[GRID] Unable to execute navigation command: invalid direction provided.')

        self.currentPos = self.nextPos
        self.setRobotPos()

        if success == 0:
            print('[GRID] Unable to execute navigation command: new grid position occupied.')
        elif success == 1:
            self.robot.drive_straight(distance_mm(250), speed_mmps(50)).wait_for_completed()

    def turn(self, rotation):
        self.nextPos[2] = self.currentPos[2] + rotation

        self.robot.turn_in_place(rotation)

        self.currentPos = self.nextPos

    def face(self, direction):
        currentHeading = self.currentPos[2]

        if direction == "north":
            headingDifference = (currentHeading - 0) * -1.0
            self.currentPos[2] = 0
        elif direction == "south":
            headingDifference = (currentHeading - 180) * -1.0
            self.currentPos[2] = 180
        elif direction == "east":
            headingDifference = (currentHeading - 90) * -1.0
            self.currentPos[2] = 90
        elif direction == "west":
            headingDifference = (currentHeading - 270) * -1.0
            self.currentPos[2] = 270
        else:
            print("[GRID] Invalid direction given to face(self, direction)")

        self.robot.turn_in_place(degrees(headingDifference)).wait_for_completed()

    def clearRobotPos(self):
        self.locGrid[self.currentPos[1]][self.currentPos[0]] = 0

    def setRobotPos(self):
        self.locGrid[self.currentPos[1]][self.currentPos[0]] = 2