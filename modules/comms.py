from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import cozmo
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import time

"""
CLASS: comms.py

Handles the communication between two Cozmos.
"""

class Comms(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[COMMS] I am the inter-robot communication controller.')

        self.robot = robot

        self.face_images = []

    # load custom markers from the directory
    async def load(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        im1_png = os.path.join(current_directory, "images", "1.png")
        im2_png = os.path.join(current_directory, "images", "2.png")
        im3_png = os.path.join(current_directory, "images", "3.png")
        im4_png = os.path.join(current_directory, "images", "4.png")
        im5_png = os.path.join(current_directory, "images", "5.png")
        im6_png = os.path.join(current_directory, "images", "6.png")
        im7_png = os.path.join(current_directory, "images", "7.png")
        im8_png = os.path.join(current_directory, "images", "8.png")
        im9_png = os.path.join(current_directory, "images", "9.png")
    # set image resolution type to bicubic
        image_settings = [(im1_png, Image.BICUBIC),
                    (im2_png, Image.BICUBIC),
                    (im3_png, Image.BICUBIC),
                    (im4_png, Image.BICUBIC),
                    (im5_png, Image.BICUBIC),
                    (im6_png, Image.BICUBIC),
                    (im7_png, Image.BICUBIC),
                    (im8_png, Image.BICUBIC),
                    (im9_png, Image.BICUBIC)]
    # load requested custom marker to represent coordinate
        for image_name, resampling_mode in image_settings:
            image = Image.open(image_name)
    # resize dimenstions of image to fit cozmo's screen
            resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)
    # invert image background to allows better recognition from the second cozmo
            face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=False)
    # display image on cozmo's face
            self.face_images.append(face_image)

    # stores custom objects in a dictionary format and assigns the coordinate values to individual types
        self.object_type_to_numberx = {CustomObjectTypes.CustomType00 : 0, CustomObjectTypes.CustomType01 : 1, CustomObjectTypes.CustomType02 : 2,
                                CustomObjectTypes.CustomType03 : 3, CustomObjectTypes.CustomType04 : 4}
        self.object_type_to_numbery = {CustomObjectTypes.CustomType05 : 5, CustomObjectTypes.CustomType06 : 6, CustomObjectTypes.CustomType07 : 7,
                                CustomObjectTypes.CustomType08 : 8, CustomObjectTypes.CustomType09 : 9}
    # define intial coordinates as 0
        self.x = None
        self.y = None

    # define custom object/marker size and the if it is unique to the world
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType00, CustomObjectMarkers.Circles2, 14, 8, 13.5, 6.35, True) 
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType01, CustomObjectMarkers.Circles3, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType02, CustomObjectMarkers.Circles4, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType03, CustomObjectMarkers.Circles5, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType04, CustomObjectMarkers.Triangles2, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType05, CustomObjectMarkers.Triangles3, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType06, CustomObjectMarkers.Triangles4, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType07, CustomObjectMarkers.Triangles5, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType08, CustomObjectMarkers.Diamonds2, 14, 8, 13.5, 6.35, True)
        await self.robot.world.define_custom_wall(CustomObjectTypes.CustomType08, CustomObjectMarkers.Diamonds3, 14, 8, 13.5, 6.35, True)
    #set image for specific duration
    def display(self, select):
        duration = 15
        image = self.face_images[select]

        self.robot.display_oled_face_image(image, duration * 1000.0)
    # clear dislpay
    def clear(self):
        duration = 0.2
        image = self.face_images[0]

        self.robot.display_oled_face_image(image, duration * 1000.0)

    # allows the second cozmo to start reading the custom marker displayed on the first cozmo
    async def read(self):
        object = None
    # run read until a custom marker is displayed on the cozmos face
        try:
            object = await self.robot.world.wait_until_observe_num_objects(1, timeout=10)

        except asyncio.TimeoutError:
            print('No object detected.')

        if object != None:
            found = True
            print(found)
    # 
        res = -1
        if found == True:
            if str(object[0].object_type) == "CustomObjectTypes.CustomType00":
                res = 0
            elif str(object[0].object_type) == "CustomObjectTypes.CustomType01":
                res = 2
            elif str(object[0].object_type) == "CustomObjectTypes.CustomType02":
                res = 4
            elif str(object[0].object_type) == "CustomObjectTypes.CustomType03":
                res = 6
            elif str(object[0].object_type) == "CustomObjectTypes.CustomType04":
                res = 7

        say = str(res) + "? Ok."
        await self.robot.say_text(say).wait_for_completed()

        print('[COMMS] Detected marker:', res)

        return res