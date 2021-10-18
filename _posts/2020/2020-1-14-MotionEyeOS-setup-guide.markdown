---
layout: post
title:  "Setting a MotionEyeOS Webcam"
date:   2020-01-15 20:12:12 -0600
categories: RaspberryPi MotionEyeOS
---

This guide is for anyone who wants to set up a MotionEye cam. You'll need a raspberry pi (I recommend a pi 3b or better, but you can get away with a 2), a \~gb sd card, raspberry pi camera and ribbon cable, and a 5v power supply.

For those who want a 3d printable case and camera holder, I recommend [this](https://www.thingiverse.com/thing:4099543) case (because I designed it and use it myself). Otherwise there plenty of commercial [options](https://amzn.to/2NFs7V3)

Besides that, the setup for MotionEyeOS is relatively easy. Although there are some tweaks that I find important to have a more functional surveillance system. We'll talk about that later.

First, go MotionEye's release [page](https://github.com/ccrisan/motioneyeos/releases). Download the corresponding images for your board. Once, downloaded plug in your preferred image flashing utility, I prefer [balenaEtcher](https://www.balena.io/etcher).

If you want to use wifi with the pi, you can drop wpa_supplicant.conf in the root directory of the sd card and paste this into the file:
```
    country=US
    update_config=1
    ctrl_interface=/var/run/wpa_supplicant
    
    network={
        scan_ssid=1
        ssid="MyWiFiSSID"
        psk="S3cr3tp@$$w0rc|"
    }
```
Be sure to replace the SSID and PSK with your SSID and password. If you have any questions or frustrations fuck off to the [git](https://github.com/ccrisan/motioneyeos/wiki/Wifi-Preconfiguration). Once this is finished, we're now done with the sd card and you can plug it into the pi.

Now for the camera. The side with the metal contacts should face toward the camera. Lift the slide clamp of the connector to make it easier to slide the ribbon cable in. Slide in the ribbon cable. Now pull it out and put it back in. Once finished slide it in again and push the clamp back. Don't use too much force. They're gentle creatures. Now for the pi connector. The process is pretty much the same. The connector you want is the one closest to the USB/Ethernet ports. Don't put it in the wrong hole. The metal contacts should face towards the HDMI port/away from the USB/Ethernet ports. 

Once this is complete, you're set to turn on the pi. The boot process takes some time to complete. You can use a network tool to monitor once the pi has come online like angryIPscanner (Windows/normie) or Nmap (linux/windows).

The login is admin and the password should be left blank. If you're not being prompted for an admin login the first time, click the person icon in the top left corner.

The First thing you should do now is change the password to something a little more secure (try password123). 

For the settings, it's important to note that this is all running on something that consumes less than 4 watts under load and has a full linux kernel and network stack. So it's not going to be able to stream and capture 1920x1080@60fps easily (I'm sure this is gonna age well). Although maybe the newer pi's can handle it better, IDGAF.

Something I like to do is enable push notifications via [Pushover](https://pushover.net/). First, enable and configure Motion Detection like so ![MotionEye Config](/assets/img/motioney_config.png).
You can set the mask to only trigger off of an area of interest like a door/entryway/shower/etc. The red-highlighted area is the area that is ignored by the camera. Also note that these settings might not work for everyone and aren't set in stone. This just works for me.

Now that motion detection is enabled go one tab down to 'Motion Notifications'. Enable Run a Command and enter as follows:
```
~ python /root/notify.py
```

Next, enable SSH server in the services tab.
Hit the annoying orange apply tab. The pi should reboot. Once the pi is back up, SSH into with a SSH client (if you've made it this far you probably know what your doing and don't need help getting one). Since the creators are complete Nazis, the entire fs is read-only so we'll need to run:
```
~ mount -o remount,rw /
~ mount -o remount,rw /boot

```
Next thing is to open /root/notify.py
```
~ nano /root/notify.py #they include nano tho?
```

Write the following python script:
```
#/usr/bin/python3
import httplib, urllib, urllib2

req = urllib2.Request('http://icanhazip.com', data=None) 
response = urllib2.urlopen(req, timeout=5)
response = response.read().strip('\n')
port = 80

conn = httplib.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
urllib.urlencode({
    "token": "APP_TOKEN",                       # Insert app token here
    "user": "USER_TOKEN",                       # Insert user token here
    "html": "1",                                # 1 for HTML, 0 to disable
    "title": "Motion Detected!",                # Title of the message
    "message": "<b>Front Door</b> camera!",     # Content of the message - include HTML if required
    "url": "http://"+response+":"+str(port),         # Link to be included in message
    "url_title": "View live stream",            # Text for the link
    "sound": "siren",                           # Define the sound played on the receiving device
}), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
```

To generate a user and app token head over to Pushover and they'll get you set up. The service costs a few bucks for an account and provides 7,500 messages/month. If your too cheap to pay that dunno why you wasted $50 on a shitty webcam. Once the tokens are added Ctrl^O and Ctrl^x and exit the SSH session. Now, download Pushover's app and you should be set to receive messages. Now try and run the following command in the SSH shell.

```
~ python /root/notify.py
```
With any luck, you should receive a push notification.

Other than that Motioneye also has Cloud storage option if you trust your data with Google/DropBox. Look at the File Storage tab if that interests you.

To keep your pi from dying a slow death, I recommend lowering the Movie/Still Quality to ~60-75%. I also have my resolution set to 720p@15fps and am mildly satisfied with it.
That's it. You survived. Adorable.