from __future__ import print_function
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import cozmo
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import time

class Comms(object):
    def __init__(self, robot: cozmo.robot.Robot):
        print('[COMMS] I am the inter-robot communication controller.')

        self.robot = robot

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

        image_settings = [(im1_png, Image.BICUBIC),
                    (im2_png, Image.BICUBIC),
                    (im3_png, Image.BICUBIC),
                    (im4_png, Image.BICUBIC),
                    (im5_png, Image.BICUBIC),
                    (im6_png, Image.BICUBIC),
                    (im7_png, Image.BICUBIC),
                    (im8_png, Image.BICUBIC),
                    (im9_png, Image.BICUBIC)]

        self.face_images = []
        for image_name, resampling_mode in image_settings:
            image = Image.open(image_name)

            resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)

            face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=False)

            self.face_images.append(face_image)

        self.object_type_to_numberx = {CustomObjectTypes.CustomType00 : 0, CustomObjectTypes.CustomType01 : 1, CustomObjectTypes.CustomType02 : 2,
                                CustomObjectTypes.CustomType03 : 3, CustomObjectTypes.CustomType04 : 4}
        self.object_type_to_numbery = {CustomObjectTypes.CustomType05 : 5, CustomObjectTypes.CustomType06 : 6, CustomObjectTypes.CustomType07 : 7,
                                CustomObjectTypes.CustomType08 : 8, CustomObjectTypes.CustomType09 : 9}
        self.x = None
        self.y = None

        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType00, CustomObjectMarkers.Circles2, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType01, CustomObjectMarkers.Circles3, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType02, CustomObjectMarkers.Circles4, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType03, CustomObjectMarkers.Circles5, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType04, CustomObjectMarkers.Triangles2, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType05, CustomObjectMarkers.Triangles3, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType06, CustomObjectMarkers.Triangles4, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType07, CustomObjectMarkers.Triangles5, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType08, CustomObjectMarkers.Diamonds2, 14, 8, 13.5, 6.35, True)
        self.robot.world.define_custom_wall(CustomObjectTypes.CustomType08, CustomObjectMarkers.Diamonds3, 14, 8, 13.5, 6.35, True)

    def display(self, select):
        duration = 5 # seconds
        image = self.face_images[select]

        self.robot.display_oled_face_image(image, duration * 1000.0)
        time.sleep(duration)

    def handleObject(self, event, **kw):
        if isinstance(event.obj, CustomObject):
            self.x = (self.object_type_to_numberx[event.obj.object_type])
        print(self.x)

    def read(self):
        self.robot.add_event_handler(cozmo.objects.EvtObjectAppeared, self.handleObject)
        time.sleep(10)