# Project Name
Use a Raspberry pi, motion sensor and a camera to build security Camera for home.

## Description
In this project, I use a raspberry pi, PIR (Passive Infrared Radar) motion sensor and a Raspberry pi camera to build a Security Camera for my home.

## Table of Contents
- [Requirements](#requirements)
- [SetUp](#setup)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements
Assumption. You have already installed the lattest verion of raspberry pi os on your raspberry pi as instructed [here](https://www.raspberrypi.com/software/)  Here is a [YouTube video](https://www.youtube.com/watch?v=sq5S1MM2Pmo) to help you
Raspberry Pi (I used a Raspberry Pi 4B)
Raspberry Pi camera (I used Raspberry Pi Camera Module V3 NOIR Wide (120 degrees))
    You do not need the NOIR Camera. I used NOIR because I wanted to capture Night vision.
    You could also use Camera V2 module which I have tested and it works fine.
Jumper Wires as needed.
A little bit of python coding skills.

## setup
Connect your raspberry pi camera [Video Help](https://youtu.be/yhM1NhD-kGs?t=34)
Connect your PIR motion Sensor [Video Help](https://www.youtube.com/watch?v=Q4_i5j64hdw)
And ssh into your raspberry pi (or connect it to your computer) or find any equivallent way of getting access to the computer.

## Usage
First clone this project.
Connect your to your raspberry pi
Choose a Service name and a user name to be used to run the project.
open the file `your_service_name.service.example` and use it to create an equivallent file `your_service_name.service` at the location at the top of that file.
For example if your service name is monitorfrontdoor, you will create a file at `/etc/systemd/system/monitorfrontdoor.service`
Also create all the other files mentioned in the `your_service_name.service.example`.

Do the same thing for `your_service_name.conf.example` for example if your project name is `monitorfrontdoor`, you will create the configuration file at `/etc/monitorfrontdoor/monitorfrontdoor.conf`.
Note: If you do not want to deal with provisioning users and accounts, you use the contents of the contents of `your_service_name.conf.example` in your `your_service_name.conf.` and when running your service, do `python capture_video_with_sensor.py debug` instead `python capture_video_with_sensor.py [production]`.
This file contains environment variables that would be used for saving your files in the cloud.
You can skip all of these and update the code to not save your video files in the cloud.
Note: if you are saving files to S3 as demonstrated in this example, you will first need to install boto3. You can do so by `sudo apt-get install python3-boto3`. Of course you will also need to provision the s3 bucket, and create the IAM user and grant them access to S3 so they can store files.

Finally, run
`python capture_video_with_sensor.py debug`
Note thave videos will be saved in your project directory and you may need to clean up occationally.

## Contributing
PRs are welcome. Propose ways to improve this. It is my pleasure.
Thank you in advance.

## License
Feel free to clone this repository and do as you wish.
