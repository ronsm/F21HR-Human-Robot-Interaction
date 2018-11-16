from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio
import cozmo
import time

class Interact(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[INTERACT] I am the interaction controller.')

        self.robot = robot

    async def detectPerson(self):
        res = False

        #await self.robot.turn_in_place(degrees(-15)).wait_for_completed()

        self.robot.move_lift(-3)
        for i in range(10, 50, 10):
            await self.robot.set_head_angle(degrees(i)).wait_for_completed()

            face = None
            firstDetect = True
        
            if face and face.is_visible and firstDetect == True:
                firstDetect = False
                self.robot.set_all_backpack_lights(cozmo.lights.blue_light)
                await self.robot.say_text("Hello There!").wait_for_completed()
                res = True
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
                except asyncio.TimeoutError:
                    print("Didn't find a face.")

            if res == True:
                break

            if i == 10:
                await self.robot.say_text("Hmm...").wait_for_completed()
            elif i == 20:
                await self.robot.say_text("Where are you?").wait_for_completed()

        return res

    async def pickupCube(self):
        #lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = await self.robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
        #lookaround.stop()

        max_dst, targ = 0, None
        for cube in cubes:
            translation = self.robot.pose - cube.pose
            dst = translation.position.x ** 2 + translation.position.y ** 2
            if dst > max_dst:
                max_dst, targ = dst, cube

            await self.robot.pickup_object(targ, num_retries=3).wait_for_completed()