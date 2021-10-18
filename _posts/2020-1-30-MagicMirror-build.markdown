---
layout: post
title:  "MagicMirror Build"
date:   2020-01-30 19:10:12 -0600
categories: Python RaspberryPi
---

Here's a little project I've worked on a few weeks ago. It's a semi-intelligent magic mirror I put together. It was relatively cheap to put together since I got the monitor for free and already had a pi lying around.

For the frame, I used this [frame](https://amzn.to/2uCL8Rk) (though when I bought it was for $100, not $150 so you may want to look elsewhere). 

The first thing to do is to make sure that the monitor works; it saves time and heartbreak. Then remove the bezel from the monitor and be careful of any ribbon cables connected to the monitor and the bezel.
For my monitor, the display was divided into two parts physically, the power supply/input logic board, and the display itself. So to keep them together I applied a hefty amount of duck tape. Because who has power tools? 

This is the final product somewhat:

![Lowkey just a selfie](/assets/img/magicmirror/front.jpg)

![Back](/assets/img/magicmirror/back.jpg)

You can't even tell its held entirely together by duck tape!

I'll explain the wizardry that is connected to the pi in a second.
To set up the magic mirror, the process is pretty automated see [here](https://github.com/sdetweil/MagicMirror_scripts).

For customizations, I like to install [3Day forecast](https://github.com/nigel-daniels/MMM-3Day-Forecast). That's pretty much it, since, I've failed repeatedly to get carousel setup. I do recommend tweaking the CSS to correct for the screen not taking up the entire mirror's real-estate.

Now here's where things get interesting. I've configured my Mirror to turn off at around 9 pm and back on at 6a m automatically. Here's how:

First, for hardware, you'll need a [photoresistor](https://amzn.to/2RWC15Z) and a [relay](https://amzn.to/37AHBRP). For tools, you'll need a soldering iron and power of will.
I've wired a photoresistor to the pi that sends a low signal whenever it detects light above a certain threshold and vice versa when it doesn't. The threshold is can be adjusted with a screw in the blue housing. I've used this in conjunction with a relay that has the control side wired to the pi and the operating side connected to a ribbon cable that was connected to the control board for the on/off buttons. Wiring is relatively simple, I've used a miniature breadboard to distribute power to the rest of the components, but isn't necessary. 

I first figured out which pins on the control board need to be shorted to turn the display on & off.
I initially planned to solder to the board, but then realized that I can scrape the plastic off of the side of the ribbon cable connecting to the board and solder directly to that.

![sketchy solder](/assets/img/magicmirror/solder.jpg)

It's sketchy but it works.

Then I plugged the soldered wires into the operating side of the relay.
Here's the code for actually toggling the pi on/off

```
#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
from time import sleep

GPIO.setmode(GPIO.BCM)

toggle = sys.argv[1]

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO is high when disp is off and GPIO low when off, inverting because that seems more logical
light_state = not GPIO.input(24) 

#will flip relay if told to turn on display and display is off or 
#if told to turn off the display and the display is on
if (toggle == "turnon" and light_state == GPIO.LOW) or (toggle == "turnoff" and light_state == GPIO.HIGH):
	GPIO.output(23, GPIO.HIGH)
	sleep(0.5)
	GPIO.output(23, GPIO.LOW)
	sleep(1.5) # wait for display to turn off
GPIO.cleanup()
```

I know. Its hot garbage. But it's my garbage. 

You can drop this script in your home directory. Make it executable with chmod.
```
~ chmod +x script.py
```
Then run crontab to create a cron job entry.
```
~ crontab -e
```

Here are my entries:

```
0	5	*	*	*	/home/pi/script.py turnon
0	21	*	*	*	/home/pi/script.py turnoff
```

What's cool about this solution is that it's easily hackable enough that you can make a webserver to toggle it on/off aswell. I've made a quick example of a flask server controlling the mirror:

```
#/usr/bin/python3

from flask import Flask,render_template
from time import sleep
import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
	light_state = not GPIO.input(24) 
	if light_state == 0:
		return render_template('index.html', color="black", state="Turn on")
	else:
		return render_template('index.html', color="white", state="Turn off")

@app.route('/test', methods=["GET"])
def button():
	light_state = not GPIO.input(24) 
	if light_state == 1:
		toggle()
		return render_template('index.html', color="black", state="Turn on")
	else:
		toggle()
		return render_template('index.html', color="white", state="Turn off")

def toggle():
	GPIO.output(23, GPIO.HIGH)
	sleep(0.5)
	GPIO.output(23, GPIO.LOW)
	sleep(1.5) # wait for display to turn off

if __name__ == '__main__':
	mirror_status = 0
	app.run(host='0.0.0.0')
	GPIO.cleanup()
```

There are other things you can do like have it toggle on whenever it senses motion or lack thereof 
The rest of the code is [here](https://github.com/leevanrell/mirror-controller.git).

Finis.