from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio
import cozmo
import time

class Interact(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[INTERACT] I am the interaction controller.')

        self.robot = robot

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
                self.robot.play_anim(name="FistBumpRequestOnce").wait_for_completed()
                break

            if i == 10:
                await self.robot.say_text("Hmm...").wait_for_completed()
            elif i == 20:
                await self.robot.say_text("Where are you?").wait_for_completed()

        return res

class reactwithcube(cozmo.objects.LightCube): #add light effect
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._chaser = None

    def start_light(self):
        if self._chaser:
            raise ValueError("Light chaser already running")
        async def _chaser():
            while True:
                for i in range(4):
                    cols = [cozmo.lights.off_light] * 4
                    cols[i] = cozmo.lights.blue_light
                    self.set_light_corners(*cols)
                    await asyncio.sleep(0.1, loop=self._loop)
        self._chaser = asyncio.ensure_future(_chaser(), loop=self._loop)

    def stop_lights(self): #stops light animation
        if self._chaser:
            self._chaser.cancel()
            self._chaser = None


# Make sure World knows how to instantiate the subclass
cozmo.world.World.light_cube_factory = reactwithcube


async def reactwithCube(self):
    cube = None
    look_around = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    try:
        cube = await self.robot.world.wait_for_observed_light_cube(timeout=60)
    except asyncio.TimeoutError:
        print("Didn't find a cube :-(")
        return
    finally:
        look_around.stop()

    cube.start_light()
    try:
        self.robot.say_text("Please tap the cube for exciting information!",play_excited_animation =True, voice_pitch=2).wait_for_completed()
        print("Waiting for cube to be tapped")
        cube.wait_for_tap(timeout=10)
        self.robot.say_text("The cube is",play_excited_animation =True, voice_pitch=2).wait_for_completed()
        print("Cube tapped")
    except asyncio.TimeoutError:
        print("No-one tapped our cube :-(")
    finally:
        cube.stop_light()
        cube.set_lights_off()