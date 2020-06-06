---
layout: post
title:  "Surviving in an offline environment"
date:   2020-06-06 17:03:36 -0600
categories: Debian Apt
---

Have you ever been so fucked that you had to work on a box that didn't have internet? Then this post is for you!

The simplest solution is to setup a squeeky clean vm and use apt to get the .debs you need. Here's an example to install wine offline:

```bash
sudo apt update -y 
sudo apt clean # just in case
sudo apt install --download-only wine # or -d
sudo zip -r wine.zip /var/cache/apt/archives/*.deb
```
Then on your offline box run:

```bash
unzip wine.zip
sudo dpkg -i *
```

This only works if the vm/online box doesn't have any of required packages installed. If you run apt -d with wine already installed then apt won't download any of the required .debs since it already sees wine installed on the system.

So what if you want to use a online dev environments with packages already installed to supply .deb packages to a offline computer?

Theres apt-offline which you can use on any system, debian or not for download your required apt packages. The problem here is that we have to install apt-offline on both the offline system and the online system. In addition to that debian 10 does not have apt-offline in it's native repos yet so we have to install it from source. 

For the online system run:
```bash
cd ~
sudo apt clean
sudo apt install git python3-pip python-magic
git clone https://github.com/rickysarraf/apt-offline.git
cd apt-offline/
mkdir soappy
cd soappy
sudo pip3 download --no-cache soappy
sudo pip3 install *
cd ..
sudo pip3 install .

```

Note we download all the required files from pip because we'll be using them later on the offline system. Now we have the online system setup, lets make a bundle to install on the offline system.
```bash
cd ~
sudo zip -r offline-install.zip /var/cache/apt/archives/*.deb apt-offline
```

Then take that over to the offline system and run:
```bash
unzip offline-install.zip
sudo dpkg -i .
cd apt-offline/soappy
sudo pip3 install *
cd ..
sudo pip3 install .
```

Now we should be set for creating a sig file for the offline system:
```bash
	sudo apt-offline set wine-offline.sig --install-packages wine
```

This generates a file to tell the online system what the offline system already has installed on it. It can use it to diff and figure out what it needs. Take the wine-offline.sig to the online system and run
```bash
sudo apt-offline get wine-offline.sig --bundle wine-install.zip
```

Then take the .zip it generates to the offline machine and run:
```bash
sudo apt-offline install wine-install.zip
```

Wasn't that fun?

The benefit of using apt-offline is allows us the flexibility of not having to use the same OS and version for the online box and allows us to install packages (on the online box) with out risking missing dependencies for the offline box.

If you are working on a system that uses yum the alternative is similar to the first process where you will need a vm with the same OS/verion and run:

```bash
	sudo yum install yum install yum-plugin-downloadonly
	yum install --downloadonly --downloaddir=<directory> <package>
```

Again this methodology is limited but it works. Sort of.

Fin.
