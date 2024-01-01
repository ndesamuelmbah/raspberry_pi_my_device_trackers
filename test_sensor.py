from gpiozero import MotionSensor
from picamera2.encoders import H264Encoder, JpegEncoder, MJPEGEncoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
from upload_to_s3 import upload_file_to_s3
import time, os, sys
from datetime import datetime, timedelta
Picamera2.set_logging(Picamera2.ERROR)

pir = MotionSensor(12)
is_capturing = False
while True:
    print("Waiting for motion...")
    pir.wait_for_motion()
    if(is_capturing):
        print("Already capturing!")
        continue
    picam2 = Picamera2()
    # Picamera2.set_logging(Picamera2.ERROR)
    # picam2.set_logging(Picamera2.ERROR)
    print("Motion detected!")
    time_now = datetime.utcnow()
    file_name = str(time_now).replace(' ', '_') + ".mp4"
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    print(f'{datetime.now()}: Video configuration:')
    encoder = H264Encoder(10000000)
    name = "H264Encoder"
    print(f'{name} {datetime.now()} Set up the time: ')
    output = FfmpegOutput(file_name, audio=False)

    print(f'{name} {datetime.now()} Set up the output: ')
    is_capturing = True
    picam2.start_recording(encoder, output)
    pir.wait_for_no_motion()
    print(f'{name} {datetime.now()} Started Recording: ')
    print(f'{name} {datetime.now()} Recording for 10 seconds:')
    picam2.stop_recording()
    picam2.close()
    is_capturing = False
    time.sleep(0.5)
    upload_file_to_s3(local_file_path=file_name, post_time=time_now, debug=True)
    print(f'{name} {datetime.now()} Recording for 10 seconds AND Done:')
    print("Motion stopped!")
