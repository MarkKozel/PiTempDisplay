#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime

import signal

import shutil #For file rename

import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



# Parse command line parameters.
# sensor_args = { '11': Adafruit_DHT.DHT11,
#                 '22': Adafruit_DHT.DHT22,
#                 '2302': Adafruit_DHT.AM2302 }
# if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
sensor = Adafruit_DHT.DHT11
pin = 18

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

csvFile = open("temp.dat", 'w')
csvFile.write("Date\tTime\tHumidity\tTemperature\n")

#Setup exit on SIG (from Pi shutdown) or CTRL
keepRunning = True

def exit_gracefully(signal, frame):
  print("Exiting due to " + str(signal))
  keepRunning = False
  csvFile.close()
  #Rename file for archive
  dt = datetime.datetime.now()
  newFileName = "temp_" + str(dt.strftime('%Y-%m-%d')) + "_" +str(dt.strftime('%H:%M:%S.%f')) + ".dat"
  print(newFileName)
  shutil.move("temp.dat", newFileName)
  #Buh-bye
  sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

#Write to file evey wtiteInterval'th time thru the forever loop
writeFlag = 0 #Keeps count of forever loop, ++'d each time thru
writeInterval = 10 #Compare current writeFlag to this to see if it is the writeInteraval'th time

while keepRunning:
  dt = datetime.datetime.now()

  # Read from sensor
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

  # Convert to F if we got good data
  if temperature is not None:
    temperature = temperature * 9/5.0 + 32

  newData = ""
  # Note that sometimes you won't get a reading and the results will be null (because Linux can't
  # guarantee the timing of calls to read the sensor).
  # If this happens try again!
  if humidity is not None and temperature is not None:
    newData = '{0}\t{1}\t{2:0.1f}\t{3:0.1f}%'.format(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M:%S'), temperature, humidity)
  else:
     newData = '{0}\t{1}\tNo Data\tNo Data'.format(dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M:%S'))
  
  #Print and Save data
  print(newData)
  if writeFlag % writeInterval is 0:
    csvFile.write(newData + "\n")
    writeFlag = 0 #Reset write flag
  else:
    writeFlag += 1 #Bump write flag for next cycle

  #Update display
  draw.rectangle((0,0,width,height), outline=0, fill=0)

  draw.text((x, top),       "Date: " + dt.strftime('%Y-%m-%d'),  font=font, fill=255)
  draw.text((x, top+8),     "Time: " + dt.strftime('%H:%M:%S'),  font=font, fill=255)
  draw.text((x, top+16),    "Temp: " + str(temperature),  font=font, fill=255)
  draw.text((x, top+25),    "Rh  : " + str(humidity),  font=font, fill=255)

  # Display image.
  disp.image(image.rotate(180))
  disp.display()

  if keepRunning is True:
    time.sleep(1)
