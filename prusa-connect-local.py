##############
# Helper script to send request to the Prusa Local Connect API
# Display the information on Adafruit's Mini PiTFT
# This file was created by André Costa from dphacks.com
# Use at your own risk
##############
import RPi.GPIO as GPIO
import requests
import json
import time
import digitalio
import board

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

GPIO.setwarnings(True) # Ignore warning for now
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Top Button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Bottom Button
GPIO.setup(22, GPIO.OUT) # Backligh IO

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

PROTOCOL='http://'
IP='192.168.1.14'
PORT='80'
ENDPOINT='/api/telemetry'
PRINTER='PRUSA Mini'

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# First define some constants to allow easy resizing of shapes.
padding = 2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Display the printer's name
y = top
draw.text((x, y), PRINTER, font=font, fill="#FF0000")
y += font.getsize(PRINTER)[1]
disp.image(image, rotation)

# Set Backlight to HIGH 
GPIO.output(22, 1)

mode = 'jobinfo'

def telemetry():

	# Send request to the printer
	r = requests.get(PROTOCOL+IP+':'+PORT+ENDPOINT)

	# Process the response 
	if r.status_code == 200: # OK
		response = r.json()
		return response
	
	else:
		# Display error message
		print(r.status_code)
		error = r.status_code
		return error


def button_callback(channel):

	global mode

	if (channel == 23) and (mode != 'progress'):
		mode = 'progress'
		#GPIO.output(22, 1) # Set Backlight to HIGH
		request_action()

	if channel == 24:
		mode = 'jobinfo'
		#GPIO.output(22, 0) # Set Backlight to LOW
		display_jobinfo()

def request_action():

	global mode

	while mode == 'progress':

		print('Mode: '+mode)
		
		if GPIO.input(24) == False:
			break

		# Draw a black filled box to clear the image.
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		
		# Send request to the printer
		r = requests.get(PROTOCOL+IP+':'+PORT+ENDPOINT)

		# Process the response 
		if r.status_code == 200: # OK
			response = r.json()
			status = "Connected"
			btemp = response["temp_bed"] # Bed temp
			ntemp = response["temp_nozzle"] # Nozzle temp
			btemp = 'Bed: '+str(btemp)+' C' # Bed temp
			ntemp = 'Nozzle: '+str(ntemp)+' C' # Nozzle temp
			
			# Check if progress is being reported.
			# API only reports progress when printing is in progress
			if "progress" in response:
				progress = response["progress"]/100
			else:
				progress = 1

			# Start at the top and add the font height
			y = top
			draw.text((x, y), PRINTER, font=font, fill="#FF0000")
			y += font.getsize(PRINTER)[1]
			draw.text((x, y), btemp, font=font, fill="#FFFFFF")
			y += font.getsize(btemp)[1]
			draw.text((x, y), ntemp, font=font, fill="#FFFFFF")
			y += font.getsize(ntemp)[1]

			# Progress bar setup
			# First, draw the outline of the progress bar
			pbar_padding = 5
			outline = 1
			oline_x = x+pbar_padding
			oline_width = width-pbar_padding
			oline_y = y+pbar_padding*2
			draw.rectangle((oline_x, oline_y, oline_width, bottom), outline=(255,255,255), fill=(0,0,0), width=outline)

			
			# Progress bar coordinates
			pbar_x = oline_x+outline
			pbar_width = (oline_width-outline)*progress
			
			# Adjust progress bar starting point
			# if the progress percentage woule make the x coordinate
			# smaller than the outline x coordinate
			if pbar_width < pbar_x:
				pbar_width = pbar_x+1

			pbar_y = oline_y+outline
			pbar_bottom = bottom-outline
			draw.rectangle((pbar_x, pbar_y, pbar_width, pbar_bottom), outline=0, fill=(255,0,0))

		else:
			# Display error message
			print(r.status_code)

		disp.image(image, rotation)

		time.sleep(10)
	
def display_jobinfo(channel):

	global mode

	mode = 'jobinfo'

	response = telemetry()

	print("Mode: "+mode)

	# Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=0)

	if isinstance(response, int) != True :
		material = response["material"]
		material = 'Material: '+material

		if "project_name" in response:
			filename = response["project_name"]
		else:
			filename = "---"

		filename = "File: "+filename

		y = top
		draw.text((x, y), PRINTER, font=font, fill="#FF0000")
		y += font.getsize(PRINTER)[1]
		draw.text((x, y), material, font=font, fill="#FFFFFF")
		y += font.getsize(material)[1]
		draw.text((x, y), filename, font=font, fill="#FFFFFF")
	else:
		errocode = "Error: "+str(response)
		y = top
		draw.text((x, y), PRINTER, font=font, fill="#FF0000")
		y += font.getsize(PRINTER)[1]
		draw.text((x, y), errocode, font=font, fill="#FFFFFF")

	disp.image(image, rotation)


GPIO.add_event_detect(23, GPIO.FALLING, callback=button_callback, bouncetime=200) # Setup event on pin 23 rising edge
GPIO.add_event_detect(24, GPIO.FALLING, callback=display_jobinfo, bouncetime=200) # Setup event on pin 24 rising edge


message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up