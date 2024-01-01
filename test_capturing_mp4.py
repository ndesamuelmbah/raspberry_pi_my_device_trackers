#!/usr/bin/python3
import time
from datetime import datetime, timedelta

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, JpegEncoder, MJPEGEncoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
print(f'{datetime.now()}: Video configuration:')
encoder = H264Encoder(10000000)
name = "H264Encoder"
print(f'{name} {datetime.now()} Set up the time: ')
output = FfmpegOutput(f'test_{name}.mp4', audio=False)

print(f'{name} {datetime.now()} Set up the output: ')

picam2.start_recording(encoder, output)
print(f'{name} {datetime.now()} Started Recording: ')
time.sleep(10)
print(f'{name} {datetime.now()} Recording for 10 seconds:')
picam2.stop_recording()
print(f'{name} {datetime.now()} Recording for 10 seconds AND Done:')

#encoders = {"H264Encoder": H264Encoder(10000000), "JpegEncoder": JpegEncoder(10000000), "MJPEGEncoder": MJPEGEncoder(10000000)}
# for name, encoder in encoders.items():
#     print(f'{name} {datetime.now()} Set up the time: ')
#     output = FfmpegOutput(f'test_{name}.mp4', audio=False)

#     print(f'{name} {datetime.now()} Set up the output: ')

#     picam2.start_recording(encoder, output)
#     print(f'{name} {datetime.now()} Started Recording: ')
#     time.sleep(10)
#     print(f'{name} {datetime.now()} Recording for 10 seconds:')
#     picam2.stop_recording()
#     time.sleep(1)
#     print(f'{name} {datetime.now()} Recording for 10 seconds AND Done:')