from gpiozero import MotionSensor
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import time, os, sys

pir = MotionSensor(12)
while True:
    print("Waiting for motion...")
    pir.wait_for_motion()
    print("Motion detected!")
    pir.wait_for_no_motion()
    print("Motion stopped!")
