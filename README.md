# Prusa Connect Mini TFT Display

Displays information from the Prusa Connect Local API on Adafruit's Mini TFT or Pimoroni's Inky pHAT e-ink display (Raspberry Pi).

Displays basic information about current print job on a Pursa Mini. It checks print progress every 10 second.

Nozzle Temp
Bed Temp
Material loaded
Progress Bar

If you would like to read some more about cameras and photography, check out my website @ [{DPHacks}](https://dphacks.com/how-to-canon-camera-control-api-ccapi/) website - a website for everything camera hack related.

## Support

```prusa-connect-local.py``` Currently it is setup to worth with Adafruit's Mini TFT Dsiplay, but it can work with any of their TFT displays.  
```inky-phat-prusa-mini.py``` Supports the Inky pHAT e-ink display.

Make sure to edit the information block below before running the script.

```
PROTOCOL='http://'
IP='192.168.1.14'
PORT='80'
ENDPOINT='/api/telemetry'
PRINTER='PRUSA Mini'
```

So far, only the ```telemetry``` api is functional on the Prusa Mini.

## Things to be aware of

These script have very little error handling. For instance there is no safeguard if you enter the wrong IP address. The script just won't work. There are also some timing issues on the displays that have built in buttons since the script is polling the printer at regular intervals. Just don't go crazy clicking buttons :).

Script is set to run forever.

## Inky pHAT display

Follow the steps outlined in this article to install the necessary libraries: [Getting Started with Inky pHAT](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811)

![Prusa Mini Raspberry Pi Inky pHAT](images/Prusa%20Raspberry%20Pi%20e-ink%20Display_01.jpg)

Use ```inky-phat-prusa-mini.py```

Either find the piece of code below and change the value to the correct color of display you have. Possible options are: "red", "yellow", and "black". The default color is "red"

```
# Default inky color
inky_color = "red"
```

Or pass an argument ```-c``` or ```--color``` when calling the script.

Example:

```python3 inky-phat-prusa-mini.py -c black```

You can use "black" on the red and yellow displays to make them refresh faster.


## Adafruit Mini PiTFT

Follow the steps outlined in this article to install the necessary libraries: [Adafruit Mini PiTFT Python Setup](https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup)

Use ```prusa-connect-local.py```

If you have a different Adafruit TFT display, change the code block below.

```
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
```

Unlike the Inky pHAT script, there are no arguments/options for this script.