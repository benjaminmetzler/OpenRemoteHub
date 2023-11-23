#! /bin/bash

currentdir=$(pwd)

echo "*** Install the necessary packages ***"
sudo apt update
sudo apt install -y git \
                    vim \
                    python3 \
                    python3-pip \
                    virtualenv \
                    evtest \
                    lirc

echo "*** Configure kernal extensions for the anava IR adapter ***"
sudo su -c "echo 'dtoverlay=gpio-ir,gpio_pin=18' >> /boot/config.txt"
sudo su -c "echo 'dtoverlay=gpio-ir-tx,gpio_pin=17' >> /boot/config.txt"

echo "*** Update the lirc to support the anava IR adapter ***"
sudo cp /etc/lirc/lirc_options.conf /etc/lirc/lirc_options.conf.backup.$(date '+%Y%m%d%H%M%S')
sudo su -c "cat /etc/lirc/lirc_options.conf | sed 's/devinput/default/g' > /etc/lirc/lirc_options.conf.new"
sudo su -c "cat /etc/lirc/lirc_options.conf.new | sed 's/auto/\/dev\/lirc0/g' > /etc/lirc/lirc_options.conf"
sudo rm /etc/lirc/lirc_options.conf.new

echo "*** enable the lircd service ***"
sudo systemctl enable lircd

echo "*** Prevent power buttons on remotes from putting the Raspberry Pi to sleep ***"
sudo su -c "echo 'HandlePowerKey=ignore' >> /etc/systemd/logind.conf"
sudo su -c "echo 'HandleSuspendKey=ignore' >> /etc/systemd/logind.conf"

echo "*** pull the OpenRemoteHub repo locally ***"
cd $currentdir
git clone https://github.com/benjaminmetzler/OpenRemoteHub.git
cd $currentdir/OpenRemoteHub
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

echo "*** copy the sample lirc IR defintion files ***"
cd $currentdir/OpenRemoteHub
sudo cp ir_database/*.conf /etc/lirc/lircd.conf.d/

# echo "*** Install and enable the OpenRemoteHub service ***"
# sudo cp OpenRemoteHub.service /etc/systemd/system/OpenRemoteHub.service
# sudo systemctl enable OpenRemoteHub

echo "*** reboot to make sure everything is up and running ***"
sudo shutdown -r 0
