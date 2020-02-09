---
layout: post
title:  "How to configure your IoT GPS modules"
date:   2020-02-09 14:02:45 -0600
categories: IoT Adafruit
---

A few years ago, I had a project that required me to collect GPS along with the db of cell towers, so I could triangulate their location. I went down the rabbit hole of configuring the GPS module to output NMEA sentences in the format I wanted; I wasted some time on it, so I decided that this might help someone avoid wasting time.

The GPS module I used is the ["Adafruit Ultimate GPS Breakout"](https://www.adafruit.com/product/746). This is a pretty decent module for the price although you can probably find knockoffs on aliexpress if you're cheap. 
When you first plug in the GPS module you'll notice that it prints a __ton__ of additional data you may or may not need. To limit what it printed to what I wanted I had to do some research on the GPS's PMTK API to figure out what I needed to do. You can find the PMTK commands for configuring it [here](https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf).

Based on that spreadsheet I've put together this little script:
```
#!/usr/bin/python3

import serial 
from time import sleep

GPS_TTY = '/dev/ttyUSB0'
print('configuring GPS')
try:
	#start tty session
    GPS_Serial = serial.Serial(port=GPS_TTY, baudrate=9600, parity=serial.PARITY_NONE, \
    	stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)  
    sleep(0.5)
    #configures GPS to only output GPGGA Sentences
    GPS_Serial.write(b'$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29<CR><LF>\r\n')
    sleep(0.5)
    #configures how often GPS prints
    GPS_Serial.write(b'$PMTK220,100*2F<CR><LF>\r\n')
    sleep(0.5)
    #set the baudrate of the GPS
    GPS_Serial.write(b'$PMTK251,115200*1F<CR><LF>\r\n')
    sleep(0.5)
    GPS_Serial.close()
except serial.SerialException as e:
    print('lost connection to GPS unit')
    GPS_Serial.close()
```

So the first thing we do is open a tty with the GPS unit; its default baud rate is at 9600, but we'll be changing that in a moment;

Now we can start sending commands to our GPS unit.
The first command is PMTK314 (PMTK_API_SET_NMEA_OUTPUT), it configures the GPS to send only sentences we care about. We tell it to write out only our GPS fix data and nothing else by setting everything to 0, except for NMEA_SEN_GGA field. As an aside, you can set the value to more than one if you wanted to have the message print every so often instead of every update period.

The next command is PMTK220 (PMTK_SET_NMEA_UPDATERATE). This command configures the update period of the GPS module. The data field is how often you want it to update in milliseconds, it can be between 100-10000.

The last command is PMTK251 (PMTK_SET_NMEA_BAUDRATE). Because we changed the update rate, we also need to change the baud rate so the tty can keep up. The data field here is just the baud rates, it is capable of 4800, 9600, 14400, 19200, 38400, 57600, 115200. We'll turn it up all the way 115200 since we like to live fast and loose.

The keener among you has probably noticed that most of these messages are followed by two digits of hex and "<CR><LF>". This is a checksum value that has to be calculated for the preceding message, if you want to customize your own GPS/messages you can use this resource [here](http://www.hhhh.org/wiml/proj/NMEAxor.html) to create your checksums.

To parse the GPGGA sentences, you can use [pyNMEA2](https://github.com/Knio/pyNMEA2). Although be sure to sanitize/authenticate the GPS's output before your try to parse, the GPS/Serial connection can fuck up and spit out bad data, which will throw exceptions and crash your script. Or if you're me, just use a massive try-catch to keep it chugging.

And as a final note, the next time you open a tty with the GPS you'll need to set the baud rate up to 115200. And if you use a coin cell battery with it you won't have to reconfigure every time it boots.

Finis.