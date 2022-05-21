#! /bin/bash
# https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md#infrared-and-lirc

currentdir=$(pwd)

echo "*** add the source files to apt ***"
sudo su -c "grep '^deb ' /etc/apt/sources.list | sed 's/^deb/deb-src/g' > /etc/apt/sources.list.d/deb-src.list"

echo "*** Install the necessary packages ***"
sudo apt update
sudo apt upgrade -y

sudo apt install -y git \
                    vim \
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

echo "*** Build the patched version of lirc for the anava IR adapter ***"
mkdir $currentdir/lirc-src
cd $currentdir/lirc-src
apt source lirc
wget https://raw.githubusercontent.com/neuralassembly/raspi/master/lirc-gpio-ir-0.10.patch
patch -p0 -i lirc-gpio-ir-0.10.patch
cd lirc-0.10.1
debuild -uc -us -b
cd $currentdir/lirc-src
sudo apt install -y ./liblirc0_0.10.1-6.3_armhf.deb ./liblircclient0_0.10.1-6.3_armhf.deb ./lirc_0.10.1-6.3_armhf.deb

echo "*** Update the lirc to support the anava IR adapter ***"
sudo cp /etc/lirc/lirc_options.conf /etc/lirc/lirc_options.conf.backup.$(date '+%Y%m%d%H%M%S')
sudo su -c "cat /etc/lirc/lirc_options.conf | sed 's/devinput/default/g' > /etc/lirc/lirc_options.conf.new"
sudo su -c "cat /etc/lirc/lirc_options.conf.new | sed 's/auto/\/dev\/lirc0/g' > /etc/lirc/lirc_options.conf"
sudo rm /etc/lirc/lirc_options.conf.new

echo "*** Configure kernal extensions for the anava IR adapter ***"
sudo su -c "echo 'dtoverlay=gpio-ir,gpio_pin=18' >> /boot/config.txt"
sudo su -c "echo 'dtoverlay=gpio-ir-tx,gpio_pin=17' >> /boot/config.txt"

echo "*** enable the lircd service ***"
sudo systemctl enable lircd

echo "*** Prevent power buttons on remotes from putting the Raspberry Pi to sleep ***"
sudo su -c "echo 'HandlePowerKey=ignore' >> /etc/systemd/logind.conf"
sudo su -c "echo 'HandleSuspendKey=ignore' >> /etc/systemd/logind.conf"

echo "*** Disable tty session to prevent the keyboard access from locking the system ***"
sudo su -c "echo 'NAutoVTs=0' >> /etc/systemd/logind.conf"
sudo su -c "echo 'eserveVT=0' >> /etc/systemd/logind.conf"
sudo systemctl disable getty@tty1.service

echo "*** pull the my_remote repo locally ***"
cd $currentdir
git clone https://github.com/benjaminmetzler/my_remote.git
cd $currentdir/my_remote
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

echo "*** Copy and activate the harmony companion map for unknown keys ***"
cd $currentdir/my_remote
sudo cp scripts/98-harmonycompanion.hwdb /etc/udev/hwdb.d/
sudo systemd-hwdb update
sudo udevadm trigger

echo "*** copy the sample lirc IR defintion files ***"
cd $currentdir/my_remote
sudo cp ir_database/*.conf /etc/lirc/lircd.conf.d/

echo "*** Install and enable the my_remote service ***"
# sudo cp my_remote.service /etc/systemd/system/my_remote.service
# sudo systemctl enable my_remote

echo "*** reboot to make sure everything is up and running ***"
sudo shutdown -r 0
