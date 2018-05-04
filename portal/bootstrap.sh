#!/bin/sh
#initial bootstrapping script

set -e


aptitude -y update
aptitude -y safe-upgrade
aptitude -y install git hostapd udhcpd wiringpi python3-virtualenv python3-dev python3-simplejson python3-urllib3 python3-rpi.gpio ntp build-essential bind9 openssh-server

#clone repo
git clone https://github.com/shackspace/Portal-v4.git /opt/Portal-v4

cp -r ../../Portal-v4 /opt/

ln -sf /opt/Portal-v4 /opt/Portal-v3

ln -sf /opt/Portal-v4 /opt/Portal

#link config files to /etc
ln -sf /opt/Portal-v4/portal/config/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

ln -sf /opt/Portal-v4/portal/config/default/hostapd /etc/default/hostapd

ln -sf /opt/Portal-v4/portal/config/udhcpd.conf /etc/udhcpd.conf

ln -sf /opt/Portal-v4/portal/config/default/udhcpd /etc/default/udhcpd

ln -sf /opt/Portal-v4/portal/config/network/interfaces /etc/network/interfaces

ln -sf /opt/Portal-v4/portal/config/bind/named.conf.local /etc/bind/named.conf.local

ln -sf /opt/Portal-v4/portal/config/bind/db.portal /etc/bind/db.portal

ln -sf /opt/Portal-v4/portal/config/rc.local /etc/rc.local

ln -sf /opt/Portal-v4/portal/config/ntp.conf /etc/ntp.conf

ln -sf /opt/Portal-v4/portal/config/cron.d/portal /etc/cron.d/portal

ln -sf /opt/Portal-v4/portal/config/ssh/sshd_config /etc/ssh/sshd_config

ln -sf /opt/Portal-v4/portal/config/systemd/check_button.service /etc/systemd/system/check_button.service

#add group portal
groupadd portal

#add user open
useradd -b /home --create-home -G dialout,portal,gpio open
mkdir /home/open/.ssh
chown open:open /home/open/.ssh
chmod 700 /home/open/.ssh

#add user close
useradd -b /home --create-home -G dialout,portal,gpio close
mkdir /home/close/.ssh
chown close:close /home/close/.ssh
chmod 700 /home/close/.ssh

#restart hostapd and udhcpd
service hostapd restart
service udhcpd restart
service bind9 restart
systemctl restart ssh.service
systemctl enable ssh.service
systemctl disable dhcpcd
systemctl enable /opt/Portal-v4/portal/config/systemd/check_button.service
systemctl start check_button.service
systemctl enable udhcpd

#add logging
mkdir -p /var/log/portal/
touch /var/log/portal/keyholder
touch /var/log/portal/portal.log
chgrp -R portal /var/log/portal
chmod -R g+rw portal /var/log/portal
