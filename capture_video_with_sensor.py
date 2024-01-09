from gpiozero import MotionSensor
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
from upload_to_s3 import upload_file_to_s3, notify_motion_detected
from sams_motion_sensor import SamsMotionSensor
import time
from datetime import datetime
Picamera2.set_logging(Picamera2.ERROR)

sensor_pin_number = 12
#pir = MotionSensor(sensor_pin_number)
pir = SamsMotionSensor(sensor_pin_number, sample_rate=10, sample_wait=1, threshold=0.2, queue_len=5, average=max)
is_capturing = False
while True:
    # print("Waiting for motion...")
    pir.wait_for_motion()
    if(is_capturing):
        continue
    notify_motion_detected()
    picam2 = Picamera2()
    print(f"{datetime.now()}: Motion detected!")
    time_now = datetime.utcnow()
    file_name = time_now.strftime('%Y-%m-%d-%H-%M-%S-%f') + ".mp4"
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    encoder = H264Encoder(10000000)
    name = "H264Encoder"
    print(f'{name} {datetime.now()} Set up the time: ')
    output = FfmpegOutput(file_name, audio=False)

    print(f'{name} {datetime.now()} Set up the output: ')
    is_capturing = True
    picam2.start_recording(encoder, output)
    pir.wait_for_no_motion()
    print(f'{name} {datetime.now()} Recording completed after {(datetime.utcnow()-time_now).total_seconds()} seconds')
    picam2.stop_recording()
    picam2.close()
    is_capturing = False
    time.sleep(1)
    upload_file_to_s3(local_file_path=file_name, post_time=time_now, debug=True)

    print(f"{datetime.now()}: Motion stopped!")
