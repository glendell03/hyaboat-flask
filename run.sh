#!/bin/bash

python3 app.py &
python3 model/detect.py --model model/efficientdet_lite0.tflite
