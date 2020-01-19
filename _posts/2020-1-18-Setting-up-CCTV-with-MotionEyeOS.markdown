---
layout: post
title:  "Setting up CCTW with MotionEyeOS "
date:   2020-01-18 19:22:12 -0600
categories: RaspberryPi MotionEyeOS
---

Recently, my paranoia of home invasion has reached a climax; So in addition to setting up a MotionEye cam pointed at my door, I've also decided I need a CCTV-like capability to monitor my door at all times while I'm at my Desk.

Assuming you already have MotionEye setup on a pi (if you don't you can look at my previous post [here](/raspberrypi/motioneyeos/2020/01/15/MotionEyeOS-setup-guide/)), you'll only need to setup a Pi 3 with the latest rasbian image. I used a Pi 3 and the [official 7-in screen](https://amzn.to/2R7u5j6). 

Once you have a raspberry pi 3 running and on a network go ahead and update it with
```
~ sudo apt update -y && sudo apt upgrade -y
```

Then install unclutter with (this is to hide the mouse-cursor, not actually required)
```
~ sudo apt install unclutter
```

Now onto the bread and butter. Make sure that you have the streaming functionality enabled, otherwise it won't work. In order to display the MotionEyeOS stream we'll make chromium load on startup and open to the motioneye's streaming page. Write the following to /home/pi/.config/lxsession/LXDE-pi/autostart.
```
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --kiosk http://{MOTIONEYE'S IP}}:8081
@unclutter -idle 0
```

If you need to rotated the display write
```
lcd_display=2
```
into /boot/config.txt, 2 rotates it by 180 degrees.

And that's it! Reboot to ensure everything is working.

![MotionEye Config](/assets/img/cctv.jpg)