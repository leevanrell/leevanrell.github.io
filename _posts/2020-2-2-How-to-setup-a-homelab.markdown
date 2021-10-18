---
layout: post
title:  "How to Setup a Homelab: Making a Parts List"
date:   2020-02-02 17:12:38 -0600
categories: Homelab ESXi
---

A few years ago, I built my first homelab server; I remember it being a bit of a daunting task and decided it might be helpful to share a few insights.

I used [r/homelabs](https://www.reddit.com/r/homelabs/) as a resource to assemble the parts list. Along with [wikipedia](https://en.wikipedia.org/wiki/List_of_Intel_Xeon_microprocessors) and intel's [spec site](https://ark.intel.com/content/www/us/en/ark.html#@PanelLabel595) for choosing the CPUs.

The initial build was this: 

```
 Intel Xeon E5-2660 v2 2.20GHz x2
 ARCTIC Alpine 20 Plus CO - 130 Watt Low Noise CPU Cooler x2
 Supermicro X9DRi-LN4F+ Dual LGA2011 1.20 Support E5-2600 v2 24x Slot DDR3 
 32GB 4X8GB DDR3 1333MHz ECC REG MEMORY x2 (64 gb total)
 Crucial BX300 120GB 
 WD Red 4tb 5400rpm HDD x4
 Phanteks Enthoo Pro series ATX Full Tower Case
 EVGA SuperNOVA 750 G2, 80+ GOLD 750W,
```

With the years came some regrets, most derived from the build itself.

Now the processors I picked are definitely good performers; however, having two beefy Xeons running 24/7 has its downsides. This is a system that will bump your electricity bill up a notch. Now, me being young and foolish at the time never really sat down and did the math. I will break it down for those reading at home. 

The average cost of power where I live is about 0.11/kWh (about the national average). Using this [site](https://forums.servethehome.com/index.php?threads/xeon-26xx-v2-power-draw.22720/) for estimating power consumption, we can estimate my power consumption to be around 120w-130w idle. For the most part, it never reaches a very high load unless I'm doing something very compute-intensive which is rare. So let's just call it on average 140Wh to round things out. 

So that means every day we consume 3.360 kWh a day. Or 100.8 kWh a month, adding about \~$11 a month to my electricity bill. Since inception that would be about $264 dollars of electricity, I would've paid for running this system in my apartment.

As a plus, It is a 'future-proofed' system that I don't foresee upgrading the CPUs anytime in the future. Unless something breaks. But I would recommend a more sane spec with just a single Xeon for the newbie who wants to get into the world of homelabing. 

Staying within the realm of power, the EVGA PSU was a good choice. It's an age-old rule of thumb to never skimp on the power supply. It's important to get a good 80plus power supply to save money. Nowadays an 80plus PSUs are much cheaper and accessible. I'm not 100% sure if it's true, but supposedly using a PSU that far exceeds what your system can consume will help preserve the life of the PSU since it'll be far less under load than less capable PSUs. It makes [sense](https://www.ee.co.za/article/thermal-stress-capacitors-failure-prevention.html) to me, but I'd take it with a grain of salt since the things most likely to fail in a PSU will still fail eventually no matter how much they've been used. 

Outside of that most choices for hardware are relatively easy. Once you've picked your CPU everything else falls in place. At first, I was apprehensive toward using used hardware, but for Processors, RAM, and even HDDs you can hardly tell. The bonus for used Xeons is there a huge over-saturation of them on the market. If you okay with not having the latest and greatest, you can acquire 2-3 generations old Xeons for less than $200. I believe I paid $250 for my two Xeons.

I think Supermicro is still a good choice for motherboards. I recommend an enterprise motherboard instead of the consumer/extremist grade ones that come out from time to time. For motherboards, the more bells and whistles you have the more likely it is to fail. That's why most server motherboards are stripped down to the bare essentials. 

As for the HyperVisor, I used the free version of ESXi, its relatively easy to set up and maintain. The webclient it provides is always useful (despite a few bugs here and there). I've also been thinking of adding a GPU for Machine learning and it seems like ESXi is still the best solution for GPU passthrough, so that's a plus.

Other options though are KVM, Proxmox, and Hyper-V. The ESXi free version has some limits on it (like no vCenter, 2 physical CPUs max, 8 vCPU/VM max), however, I feel like it isn't a big deal for most non-commercial/enterprise users. Realistically, none of these options is a bad choice, it's down to what you prefer.

As a note, if you chose to use a dual-socket motherboard and a tower instead of a rack solution, be wary of the dimensions; it was a tight squeeze getting my motherboard in its case.

That's it for now.