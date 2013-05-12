# Retrocade

A quick and dirty rom selector for my arcade machine running on a Raspberry Pi.

The repository holds the code for the rom selector, but this README includes the full instructions for getting the Raspberry Pi setup and installed.

## Setup

My Pi uses the Raspian distro. So get that installed and then run:

	sudo aptitude update
	sudo aptitude upgrade
	sudo aptitude install git

### dgen

	wget -O dgen.tar.gz http://downloads.sourceforge.net/project/dgen/dgen/1.32/dgen-sdl-1.32.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fdgen%2Ffiles%2Fdgen%2F1.32%2F&ts=1368376336&use_mirror=garr
	tar xvfz dgen.tar.gz
	cd dgen-sdl-1.32
	./configure --disable-opengl
	make && sudo make install

### dispmanx

	cd
	wget https://github.com/vanfanel/SDL12-kms-dispmanx/archive/master.zip 
	unzip master.zip
	cd SDL12-kms-dispmanx-master
	export CFLAGS="-I/opt/vc/include/interface/vmcs_host/linux"
	./MAC_ConfigureDISPMANX.sh
	make && sudo make install

### retrocade

	sudo aptitude install python-virtualenv
	sudo aptitude install python-dev
	git clone git://github.com/davidwinter/retrocade.git
	cd retrocade
	virtualenv env
	env/bin/pip intall urwid

## Running on boot

So that we can get retrocade starting on bootup, we need to enable auto-login:

### dgen preference file
	
	mkdir .dgen
	cp retrocade/dgenrc .dgen/

### Autologin

	sudo nano /etc/inittab

Find the line starting with: `1:2345:respawn:/sbin/getty`

Comment it out by placing a `#` at the start. Then below that line, add:

	1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1

### Start script

Login as the `pi` user, and then `nano .bashrc`. At the bottom of this file, add:

	if [ $(tty) == /dev/tty1 ]; then
	        retrocade/env/bin/python retrocade/retro.py path/to/dgen path/to/roms
	fi

Make sure you change the paths for `dgen` and the directory containing your roms. In my case, it's just `dgen` and `/home/pi/roms`.