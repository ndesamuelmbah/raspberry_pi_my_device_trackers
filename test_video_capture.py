from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import time
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)
output = "test.mp4"
picam2.start_recording(encoder, output, quality=Quality.HIGH)
time.sleep(10)
picam2.stop_recording()
