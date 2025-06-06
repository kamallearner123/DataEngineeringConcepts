import RPi.GPIO as gpio
import time
import os
import sys
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime
from picamera import PiCamera

# GPIO Setup
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# --- GPIO Classes ---
class PinIn:
    def __init__(self, pin_num):
        gpio.setup(pin_num, gpio.IN)
        self.pin = pin_num

    def get(self):
        return gpio.input(self.pin)

class PinOut:
    def __init__(self, pin_num):
        gpio.setup(pin_num, gpio.OUT)
        self.pin = pin_num

    def on(self):
        gpio.output(self.pin, gpio.HIGH)
        print(f"Pin {self.pin} is ON")

    def off(self):
        gpio.output(self.pin, gpio.LOW)
        print(f"Pin {self.pin} is OFF")

# --- Camera Class ---
class Camera:
    def __init__(self):
        self.cam = PiCamera()

    def capture_pic(self):
        timestamp = datetime.now()
        filename = timestamp.strftime("%d_%m_%Y_%H_%M_%S.jpg")
        self.cam.start_preview()
        time.sleep(1)
        self.cam.capture(filename)
        self.cam.stop_preview()
        return filename

    def record_video(self, secs):
        timestamp = datetime.now()
        filename = timestamp.strftime("%d_%m_%Y_%H_%M_%S.h264")
        self.cam.start_preview()
        self.cam.start_recording(filename)
        time.sleep(secs)
        self.cam.stop_recording()
        self.cam.stop_preview()
        return filename

# --- Email Function ---
def send_mail(filename):
    with open(filename, "rb") as img_file:
        img_data = img_file.read()

    timestamp = datetime.now().strftime("%A %B %d %Y @ %H:%M:%S")
    msg = MIMEMultipart()
    msg["Subject"] = f"Motion Detected - {timestamp}"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "receiver_email@gmail.com"

    msg.attach(MIMEText("WARNING! Motion Detected! Decide to give access."))
    msg.attach(MIMEImage(img_data, name=os.path.basename(filename)))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        server.sendmail(msg["From"], msg["To"], msg.as_string())

# --- Main Program ---
if __name__ == "__main__":
    cam = Camera()
    led_green = PinOut(14)
    led_red = PinOut(15)
    led_blue = PinOut(18)
    switch = PinIn(24)

    while True:
        if switch.get() == gpio.HIGH:
            led_green.off()
            led_red.off()
            led_blue.off()

            pic_name = cam.capture_pic()
            print("Picture captured:", pic_name)
            send_mail(pic_name)

            vid_name = cam.record_video(10)
            print("Video recorded:", vid_name)

            time.sleep(1)
        else:
            led_red.on()
            led_green.on()
            led_blue.on()
            time.sleep(1)

