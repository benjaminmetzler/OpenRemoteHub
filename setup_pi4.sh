#! /bin/bash
# https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md#infrared-and-lirc

# Install the necessary packages
sudo su -c "grep '^deb ' /etc/apt/sources.list | sed 's/^deb/deb-src/g' > /etc/apt/sources.list.d/deb-src.list"
sudo apt update
sudo apt upgrade -y
sudo apt install -y vim \
                    devscripts \
                    dh-exec \
                    doxygen \
                    expect \
                    libasound2-dev \
                    libftdi1-dev \
                    libsystemd-dev \
                    libudev-dev \
                    libusb-1.0-0-dev \
                    libusb-dev \
                    man2html-base \
                    portaudio19-dev \
                    socat \
                    xsltproc \
                    python3-yaml \
                    dh-python \
                    libx11-dev \
                    python3-dev \
                    python3-setuptools \
                    python3-pip \
                    adb

# Build the patched version of lirc for the anava IR adapter
mkdir ~/lirc-src
pushd ~/lirc-src
apt source lirc
wget https://raw.githubusercontent.com/neuralassembly/raspi/master/lirc-gpio-ir-0.10.patch
patch -p0 -i lirc-gpio-ir-0.10.patch
cd lirc-0.10.1
debuild -uc -us -b
cd ~/lirc-src
sudo apt install -y ./liblirc0_0.10.1-6.3~deb10u1_armhf.deb ./liblircclient0_0.10.1-6.3~deb10u1_armhf.deb ./lirc_0.10.1-6.3~deb10u1_armhf.deb

# Update the lirc to support the anava IR adapter
sudo cp /etc/lirc/lirc_options.conf /etc/lirc/lirc_options.conf.backup.$(date '+%Y%m%d%H%M%S')
sudo su -c "cat /etc/lirc/lirc_options.conf | sed 's/devinput/default/g' > /etc/lirc/lirc_options.conf.new"
sudo su -c "cat /etc/lirc/lirc_options.conf.new | sed 's/auto/\/dev\/lirc0/g' > /etc/lirc/lirc_options.conf"
sudo rm /etc/lirc/lirc_options.conf.new # cleanup

# Configure kernal extensions for the anava IR adapter
sudo su -c "echo 'dtoverlay=gpio-ir,gpio_pin=18' >> /boot/config.txt"
sudo su -c "echo 'dtoverlay=gpio-ir-tx,gpio_pin=17' >> /boot/config.txt"

# enable the lircd service
sudo systemctl enable lircd

# install the my_remote python required packages
popd
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Prevent power buttons on remotes from putting the Raspberry Pi to sleep
sudo su -c "echo 'HandlePowerKey=ignore' >> /etc/systemd/logind.conf"
sudo su -c "echo 'HandleSuspendKey=ignore' >> /etc/systemd/logind.conf"

# Disable tty session to prevent the keyboard access from the remote
# from locking the system
sudo su -c "echo 'NAutoVTs=0' >> /etc/systemd/logind.conf"
sudo su -c "echo 'eserveVT=0' >> /etc/systemd/logind.conf"
systemctl disable getty@tty1.service

# copy the sample lirc IR defintion files
sudo cp ir_database/*.conf /etc/lirc/lircd.conf.d/

# Install and enable the my_remote service
sudo cp my_remote.service /etc/systemd/system/my_remote.service
sudo systemctl enable my_remote

# make sure everything is up and running
sudo shutdown -r 0
