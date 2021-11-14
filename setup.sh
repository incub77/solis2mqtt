#!/bin/bash

echo "### Installing pip3 ###"
apt install python3-pip

echo "### Installing requirements ###"
pip3 install -r requirements.txt

echo "### Creating config file ###"
cp /opt/solis2mqtt/config.yaml.minimal /opt/solis2mqtt/config.yaml

echo "### Creating service user ###"
addgroup --system solis2mqtt
adduser --system --no-create-home --ingroup solis2mqtt solis2mqtt
# to get access to /dev/ttyUSB*
usermod -a -G dialout solis2mqtt

echo "### Changing ownership ###"
chown -R solis2mqtt:solis2mqtt /opt/solis2mqtt

echo "### Creating run directory ###"
mkdir /run/solis2mqtt
chown -R solis2mqtt:solis2mqtt /run/solis2mqtt

echo "### Setting up systemd ###"
cp /opt/solis2mqtt/provisioning/etc/systemd/system/solis2mqtt.service /etc/systemd/system/
systemctl enable solis2mqtt



