# PiTempDisplay
Grab Temp/RH from DHT11 and display on PiOLED 128x32

## Hardware
Raspberry Pi 3B+ - although use using generic Python with common libraries, so it should work on most Pis

DHT-11 Temperature/Humidity Sensor - Just had it laying around

PiOLED 128x32 lcs display - Also just laying around

Configured I2C on Pi for display

## Software
Raspian Stretch Lite

build-essential

python-dev

python-pip

RPi.GPIO

python-imaging

python-smbus

[Adafruit_Python_SSD1306](https://github.com/adafruit/Adafruit_Python_SSD1306.git)

## Helpful Info
[Setup and Usage of Pi OLED](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
[Wiring and Coding for DHT11/22](https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/)

## Configure the Pi
Follow instructions for Setup and Usage of Pi OLED and Wiring and Coding for DHT11/22

Run tempMain.py

### Notes
I added the ``disp.image(image.rotate(180))`` because the way the PiOLED connects to the GPIO Header. The power port on the Pi is opposite the GPIO Header, so I cannot set the Pi on edge so that the PiOLED is right-side up with power plugged in. #SoftwareToTheRescue

I refered to [Run a Program On Your Raspberry Pi At Startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) to decide how to make this program run at startup. I chose [Method 4, systemd](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd) because I want this running always. And, I'm pretty comfortable with ``systemcrt`` process management