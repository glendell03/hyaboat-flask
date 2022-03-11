# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import time

import cv2, queue as Queue, threading, time
from model.object_detector import ObjectDetector
from model.object_detector import ObjectDetectorOptions
import model.utils as utils
import numpy as np


def run(
    model: str,
    camera_id: int,
    width: int,
    height: int,
    num_threads: int,
    enable_edgetpu: bool,
    relay,
    motor,
    servo,
) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
      model: Name of the TFLite object detection model.
      camera_id: The camera id to be passed to OpenCV.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
      num_threads: The number of CPU threads to run the model.
      enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """

    # Variables to calculate FPS
    counter, fps = 0, 0
    # start_time = time.time()
    q = Queue.Queue()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    # fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.3,
        max_results=2,
        enable_edgetpu=enable_edgetpu,
    )
    detector = ObjectDetector(model_path=model, options=options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            sys.exit(
                "ERROR: Unable to read from webcam. Please verify your webcam settings."
            )
        if not q.empty():
            try:
                q.get_nowait()
            except Queue.Empty:
                pass
        q.put(image)

        counter += 1
        image = cv2.flip(image, 1)

        # Run object detection estimation using the model.
        detections = detector.detect(image)
        coords = detector.getCoords()

        # Draw keypoints and edges on input image
        image = utils.visualize(image, detections)

        # Calculate the FPS
        # if counter % fps_avg_frame_count == 0:
        #     end_time = time.time()
        #     fps = fps_avg_frame_count / (end_time - start_time)
        #     start_time = time.time()

        # Show the FPS
        # fps_text = "FPS = {:.1f}".format(fps)
        # print(f"{fps_text} coords: {coords}")

        y_axis_center = height / 2
        x_axis_center = width / 2
        left_point = coords["left"]
        right_point = coords["right"]
        top_point = coords["top"]
        bottom_point = coords["bottom"]

        object_x_center = (left_point + right_point) / 2
        object_y_center = (top_point + bottom_point) / 2
        b = x_axis_center - object_x_center
        a = y_axis_center - object_y_center

        res = np.arctan2(a, b) * 180 / np.pi

        # Stop the program if the ESC key is pressed.
        # if cv2.waitKey(1) == 27:
        #     break
        # cv2.imshow("object_detector", image)
        try:
            relay.turnOn()
            motor.forward(1, 1)
            if res >= 0 and bottom_point > y_axis_center:
                rounded_res = np.round(res)
                servo.angle(rounded_res)
                # print(rounded_res)
        except KeyboardInterrupt:
            relay.turnOff()
            motor.full_stop(0.15)

    cap.release()
    cv2.destroyAllWindows()


def main(relay, motor, servo):
    t = threading.Thread(
        target=run,
        args=(
            "model/efficientdet_lite0.tflite",
            int(0),
            640,
            480,
            int(4),
            bool(False),
            relay,
            motor,
            servo,
        ),
    )

    t.start()
