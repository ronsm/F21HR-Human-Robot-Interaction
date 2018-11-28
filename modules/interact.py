from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.objects import LightCube2Id
import asyncio
import cozmo
import time

"""
CLASS: interact.py

Houses all of the key interactive elements, between robots and with humans.
"""
class Interact(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[INTERACT] I am the interaction controller.')
    # set specific cube to use, by calling their ID's
        self.robot = robot
        self.cube = robot.world.get_light_cube(LightCube2Id)

        if self.cube is not None:
            self.cube.set_lights(cozmo.lights.red_light)
        else:
            cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

    # search for cube within sight, pick up if found
    async def pickupCube(self):
        cubes = await self.robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
    # centre the robot to the cube to prepare for pick up
        max_dst, targ = 0, None
        for cube in cubes:
            translation = self.robot.pose - cube.pose
            dst = translation.position.x ** 2 + translation.position.y ** 2
            if dst > max_dst:
                max_dst, targ = dst, cube
    # pick up the cube
            await self.robot.pickup_object(targ, num_retries=3).wait_for_completed()
    # search for a face, once detected voice a confirmation with cozmo
    async def detectPerson(self):
        res = False

        #await self.robot.turn_in_place(degrees(-15)).wait_for_completed()

    # set cozmos lift to down position and head angle to 10 and 50 degrees
        self.robot.move_lift(-3)
        for i in range(10, 50, 10):
            await self.robot.set_head_angle(degrees(i)).wait_for_completed()
    # set face and detection initials
            face = None
            firstDetect = True
    # face is detected and cozmo's voices a conformation that it has detected a face
            if face and face.is_visible and firstDetect == True:
                firstDetect = False
                self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                await self.robot.say_text("Hello There!").wait_for_completed()
                res = True
                return res
            if face and face.is_visible and firstDetect == False:
                self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                time.sleep(3)
                break
            else:
                self.robot.set_backpack_lights_off()

                try:
                    face = await self.robot.world.wait_for_observed_face(timeout=5)
                    if(face):
                        self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                        await self.robot.say_text("Hello There!").wait_for_completed()
                        await asyncio.sleep(2)
                        self.robot.set_all_backpack_lights(cozmo.lights.off_light)
                        res = True
                        return res
                except asyncio.TimeoutError:
                    print("Didn't find a face.")

            if res == True:
                return res

            if i == 10:
                await self.robot.say_text("Hmm...").wait_for_completed()
            elif i == 20:
                await self.robot.say_text("Where are you?").wait_for_completed()

        return res

    # interact with the user when face is found
    async def cubeChat(self):
    # set colour of cube to blue
        self.cube.set_lights(cozmo.lights.blue_light)
        await asyncio.sleep(1)
        # voice an instruction with cozmo then wait for instruction to be completed by user 
        try:
            await self.robot.say_text("Please tap the cube for exciting information!",play_excited_animation =True, voice_pitch=2).wait_for_completed()
            print("Waiting for cube to be tapped")
            await self.cube.wait_for_tap(timeout=30)
            await self.robot.say_text("This cube belongs to me but I share it with my friend Phil, without him i wouldn't of got it back! I can manipulate and control the colours of the cube, take a look!",play_excited_animation =True, voice_pitch=2).wait_for_completed()
            print("Cube tapped")
            # transtion between RGB
            self.cube.set_lights(cozmo.lights.red_light)
            await asyncio.sleep(1)
            self.cube.set_lights(cozmo.lights.green_light)
            await asyncio.sleep(1)
            self.cube.set_lights(cozmo.lights.blue_light) 
            await asyncio.sleep(2)
            await self.robot.say_text("Isn't it wonderful!").wait_for_completed()
            await asyncio.sleep(2)
        except asyncio.TimeoutError:
            print("No-one tapped our cube :-(")
        finally:
            self.cube.set_lights(cozmo.lights.blue_light)