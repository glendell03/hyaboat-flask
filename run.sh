#!/bin/bash

python3 app.py &
python3 model/detect.py --model model/water-hyacinth-model.tflite
