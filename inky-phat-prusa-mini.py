##############
# Helper script to send request to the Prusa Local Connect API
# Display the information on an Inky pHAT e-ink display
# This file was created by André Costa from dphacks.com
# Use at your own risk
##############
import time
import datetime
import sys
import getopt
import requests
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

PRINTER="PRUSA Mini"
REFRESH=300
PROTOCOL='http://'
IP='192.168.1.14'
PORT='80'
ENDPOINT='/api/telemetry'

#default padding between 
padding = 5

# Default inky color
inky_color = "red"

# Get passed arguments
argv = sys.argv[1:]


try:
	opts, args = getopt.getopt(argv,"hc:r:",["color=", "refresh="])
except getopt.GetoptError:
	print('paramerters: -c <color> or --color <color>')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print(' -c <color> or --color <color>')
		print('Possible colors: red, yellow, or black.')
		print('Choose the color that matches your screen.')
		sys.exit()
	elif opt in ("-c", "--color"):
		inky_color = arg
	elif opt in ("-r", "--refresh"):
		REFRESH = int(arg)


inky_display = InkyPHAT(inky_color)
inky_display.set_border(inky_display.WHITE)

# Convert color to variable value
inky_color = "inky_display."+inky_color.upper()
inky_color = eval(inky_color)

# Create a blank image the size of the display
# "P" Mode - 8-bit pixels, mapped to any other mode using a color palette
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

def connect_local_telemetry():

	# Send request to the printer

	r = requests.get(PROTOCOL+IP+':'+PORT+ENDPOINT, timeout=10)

	# Process the response 
	if r.status_code == 200: # OK
		response = r.json()
		return response
	
	else:
		# Display error message
		print(r.status_code)
		error = r.status_code
		return error



def show_screen(response):

	if isinstance(response, int) != True :
		status = "Connected"
		bedlabel = "Bed"
		bedtemp = str(response["temp_bed"]) # Bed temp
		nozzlelabel = "Nozzle"
		nozzletemp = str(response["temp_nozzle"]) # Nozzle temp
		estlabel = "Est."

		# Check if progress is being reported.
		# API only reports progress when printing is in progress
		if "progress" in response:
			progress = response["progress"]
		else:
			progress = 100

		if "time_est" in response:
			esttime = response["time_est"]
			currtime = datetime.datetime.today()
			esttime = currtime + datetime.timedelta(seconds=int(esttime))
			esttime = esttime.strftime("%H:%M")
		else:
			esttime = "--:--"

	# Create a blank image the size of the display
	# "P" Mode - 8-bit pixels, mapped to any other mode using a color palette
	img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	draw = ImageDraw.Draw(img)

	font = ImageFont.truetype(FredokaOne, 22)

	y = padding

	# Add the printer name to the canvas
	#draw.text((10, y), PRINTER, inky_display.RED, font)
	draw.text((10, y), PRINTER, inky_color, font)

	# Find with of label, add label's initial x and add more padding
	progress_x = font.getsize(PRINTER)[0]+10+20
	progress_y = 10

	# Dray percentage
	font = ImageFont.truetype(FredokaOne, 18)
	draw.text((progress_x, progress_y), "{:.0f}".format(progress)+"%", inky_display.BLACK, font)

	y += font.getsize(PRINTER)[1]+padding

	font = ImageFont.truetype(FredokaOne, 15)

	draw.text((20, y), bedlabel, inky_display.BLACK, font)

	draw.text((75, y), nozzlelabel, inky_display.BLACK, font)

	draw.text((140, y), estlabel, inky_display.BLACK, font)

	y += font.getsize(bedlabel)[1]+padding

	font = ImageFont.truetype(FredokaOne, 22)

	draw.text((20, y), bedtemp, inky_color, font)

	draw.text((75, y), nozzletemp, inky_color, font)

	draw.text((140, y), esttime, inky_color, font)

	y += font.getsize(bedtemp)[1]+padding

	pbar_width = (inky_display.WIDTH-10)*progress/100
	pbar_height = inky_display.HEIGHT-padding
	draw.rectangle([10, y, pbar_width, pbar_height], fill=inky_display.RED, outline=None)

	inky_display.set_image(img)
	inky_display.show()

def show_error(e):
	
	print(e)

	# Create a blank image the size of the display
	# "P" Mode - 8-bit pixels, mapped to any other mode using a color palette
	img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	draw = ImageDraw.Draw(img)

	font = ImageFont.truetype(FredokaOne, 22)
	
	y = padding

	# Add the printer name to the canvas
	draw.text((10, y), PRINTER, inky_color, font)

	y += font.getsize(PRINTER)[1]+padding

	font = ImageFont.truetype(FredokaOne, 15)

	draw.text((10, y), e, inky_display.BLACK, font)

	inky_display.set_image(img)
	
	inky_display.show()

while True:
	try:
		telemetry = connect_local_telemetry()
	#except requests.exceptions.RequestException as e:  # This is the correct syntax
	except requests.exceptions.Timeout as e:
		error = "Connection Timed Out"
		show_error(error)
	except requests.exceptions.HTTPError as httpCode:
		show_error("Http Error:",httpCode)
	except requests.exceptions.RequestException as e:
		# catastrophic error. bail.
		raise SystemExit(e)
	else:
		show_screen(telemetry)

	time.sleep(REFRESH)


