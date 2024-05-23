import numpy as np
import cv2

from utils.intel_realsense_camera import IntelRealsenseCamera

# -------------------- Variables -------------------- 

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640

AUDIO_MESSAGE_PER_SECOND = 0.5

# -------------------- Intel Realsense Configuration -------------------- 

intel_realsense_camera = IntelRealsenseCamera(IMAGE_WIDTH, IMAGE_HEIGHT)
intel_realsense_camera.start()

try:

    while True:

        frames = intel_realsense_camera.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Normalizing depth image

        cv2.imshow('color_image', color_image)

        height, width = depth_image.shape

        # pixel size = 2 * tan ( horiz.fov /2 ) * (distance in mm / image width in pixels).

        depth_image_quotion = np.where(True, depth_image/width, depth_image/width)

        HORIZONTAL_FOV = 69

        pixel_size = (2 * np.deg2rad(HORIZONTAL_FOV / 2) )* depth_image_quotion

        cv2.imshow('pixel_size', pixel_size)

        print(f'mean: {pixel_size.mean()} max: {pixel_size.max()} min: {pixel_size.min()}')

        if cv2.waitKey(1) > -1:
            break

    
finally:
    intel_realsense_camera.stop()



