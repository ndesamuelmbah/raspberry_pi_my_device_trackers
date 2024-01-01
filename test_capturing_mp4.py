#!/usr/bin/python3
import time
from datetime import datetime, timedelta

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
print(f'{datetime.now()}: Video configuration:')
encoder = H264Encoder(10000000)
print(f'{datetime.now()} Set up the time: ')
output = FfmpegOutput('test.mp4', audio=False)

print(f'{datetime.now()} Set up the output: ')

picam2.start_recording(encoder, output)
print(f'{datetime.now()} Started Recording: ')
time.sleep(10)
print(f'{datetime.now()} Recording for 10 seconds:')
picam2.stop_recording()
print(f'{datetime.now()} Recording for 10 seconds AND Done:')