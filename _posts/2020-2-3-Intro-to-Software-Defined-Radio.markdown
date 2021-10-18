---
layout: post
title:  "Intro to Software Defined Radio: Part I"
date:   2020-02-03 19:30:24 -0600
categories: SDR gnuradio
---

For the past 4 years or so I've tinkered with Software Defined Radios (SDR), but until recently my knowledge of them was fairly limited. So, today I hope to impart some of my wisdom onto you. 

First, a __very__ brief 101 on what Software Defined Radios are and how they work. 

SDRs are everywhere, they can be found in phones, IoT devices, Cars, etc.. The thing that makes them so desirable is the flexibility they can offer manufacturers and users. In a world with constantly evolving wireless standards and protocols, it's useful to be able to update your software for free instead of having to buy new compatible hardware. There are a whole host of benefits, but that's just off the top of my head.

But how does it work? Heres a diagram I mercilessly stole from Wikipedia:

![SDR Screen](/assets/img/sdr/wiki.png)

The logic of the radio is offloaded to software where a programmer can design and implement the radio using their favorite programming language (python/c++/matlab/etc.). The software uses an API supported by the FPGA inside of the SDR, where the FPGA acts as a middle-man between the user and the RF frontend. There are a lot more physics and components that exist to manage the internal signals to make things work but that's the gist of it from a programmer's perspective.

It's hard to talk about SDR without mentioning gnuradio.
For the most part, gnuradio is the defacto framework for developing your own SDR Tools/Transmitters/Receivers/Whatever.

If you want to get started using gnuradio, let me clear somethings up. Don't install gnuradio from the default repos. They're outdated and who wouldn't want the __curved lines__ available in GRv3.8. Use gnuradio's PPA instead:
```
#!/binb/bash
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt-get update
sudo apt install gnuradio
```

As a side note, for out-of-tree modules, install from source, don't use PyBOMBs. No one uses that shit. I've been to the conference, trust me. 
To install a OOT module, its almost always the same:
```
#!/bin/bash

git clone <module>
cd <module>
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig 
```

A few OOT modules I recommend are:
* gr-baz : this a RF reverse engineering module. slightly outdated and hard to use but very cool blocks.
* gr-satellites : this is a collection of receiver/decoder/demod blocks for literally dozens of satellites
* gr-adsb : because who wouldn't want to monitor planes

There are many, many others but this is just what I remember now. Be wary of some blocks (In or Out of tree) because some of them just don't work properly; be prepared to hack shit together, then feel free to make a pull request whenever you fix their shit. Be aware that some of these modules may not yet be ported to the newest version of gnuradio.

For those who want to be badass and program a block from the ground up. Here's my recommendation, use C++. I know you want to use python; everyone wants to use python. Just trust me. What little [documentation](https://www.gnuradio.org/doc/doxygen/) exists is almost entirely on C++. And the python API isn't fully featured, meaning that everything that is implemented in C++ may not be accessible/have an equivalent in python. Just gonna have to grit your teeth and push on.

For those in the market for a SDR, there are two major factors: to transmit or not to transmit? and budget.

For those who want to transmit, the Hackrf is a good budget choice, the only problem is that it's only half-duplex, so you can only send OR receive. I would also recommend the LimeSDR, which is full-duplex, but keep in mind it is in high demand and hard to find in stock. Also, keep within all laws and regulations of the FCC. Don't transmit in bands your not allowed to. Ham licenses are easy to acquire so please get one.

For those who just want to receive, really any RTL-SDR/DVB-Tuner will work. They're are all the same for the most part. They all contain Realtek chips, R820T or RTL2832U. Some of the more expensive RTL-SDRs use better components for greater stability/frequency range; but someone new to SDR, the $20 DVB-T tuner will suit you well.

For those who want Duplex capability or higher bandwidth, Ettus makes excellent hardware for a home RF lab if you gothave the cash. 

When it comes to SDRs and price, the sky is the limit to what you want to spend. And there is no shortage of options to pick from. For the most part, it is a usually trade-off for features and cost. There are many SDRs I haven't listed, but these are just what I have experience with.

Till next time. 