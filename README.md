# Prusa Connect Mini TFT Display

Displays information from the Prusa Connect Local API on Adafruit's Mini TFT (Raspberry Pi)

Displays basic information about current print job on a Pursa Mini. It checks print progress every 10 second.

Nozzle Temp
Bed Temp
Material loaded
Progress Bar

If you would like to read some more about cameras and photography, check out my website @ [{DPHacks}](https://dphacks.com/how-to-canon-camera-control-api-ccapi/) website - a website for everything camera hack related

## Support

```prusa-connect-local.py``` Currently it is setup to worth with Adafruit's Mini TFT Dsiplay, but it can work with any of their TFT displays
```inky-phat-prusa-mini.py``` Supports the Inky pHAT e-ink display

Make sure to edit the information block below before running the script

```
PROTOCOL='http://'
IP='192.168.1.14'
PORT='80'
ENDPOINT='/api/telemetry'
PRINTER='PRUSA Mini'
```

So far, only the ```telemetry``` api is functional on the Prusa Mini

## Things to be aware of

These script have very little error handling. For instance there is no safeguard if you enter the wrong IP address. The script just won't work. There are also some timing issues on the displays that have built in buttons since the script is polling the printer at regular intervals. Just don't go crazy clicking buttons :)