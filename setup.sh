#!/bin/bash

echo "Creating config file"
cp config.yaml.minimal config.yaml

echo "Creating service user"
addgroup --system solis2mqtt
adduser --system --no-create-home --ingroup solis2mqtt solis2mqtt
usermod -a -G dialout solis2mqtt

echo "Changing ownership"
chown -R solis2mqtt:solis2mqtt .

echo "Creating runtime directory"
mkdir /run/solis2mqtt
chown -R solis2mqtt:solis2mqtt /run/solis2mqtt

echo "Setting up systemd"
cp ./provisioning/etc/systemd/system/solis2mqtt.service /etc/systemd/system/
systemctl enable solis2mqtt



