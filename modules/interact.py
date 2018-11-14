from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio
import cozmo
import time

class Interact(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[INTERACT] I am the interaction controller.')

        self.robot = robot

    def detectPerson(self):
        self.robot.move_lift(-3)
        self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

        face = None
        firstDetect = True
        
        while True:
            if face and face.is_visible and firstDetect == True:
                firstDetect = False
                self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                self.robot.say_text("Hello!").wait_for_completed()
            if face and face.is_visible and firstDetect == False:
                self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                time.sleep(3)
                break
            else:
                self.robot.set_backpack_lights_off()

                try:
                    face = self.robot.world.wait_for_observed_face(timeout=20)
                except asyncio.TimeoutError:
                    print("Didn't find a face.")
                    return

            time.sleep(.1)

        self.robot.say_text("DONE")