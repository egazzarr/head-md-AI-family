nano ~/.bashrc
lsusb
aplay -l
lsof /dev/snd/*
kill -9 2242


activating python env
source Desktop/family/aifam/bin/activate

MIC
arecord -l
TO TEST
arecord -D plughw:2,0 -f S16_LE -r 48000 -c 1 -vv /dev/null
arecord -D plughw:2,0 -r 48000 -f S16_LE -c 1 test.wav

STEPS
OFF     ON      OFF     1/8 step

CURRENT
1.0     1.2     ON      OFF     ON

500 very fast, 4000 very slow

check all inputs into raspberry
ls /dev/tty*
ls /dev/serial/by-id/
usb-Arduino__www.arduino.cc__0043_0353637333235190F161-if00  usb-Arduino__www.arduino.cc__0043_0353638323635141C072-if00

CATAPULTE
usb-Arduino__www.arduino.cc__0043_0353638323635141C072-if00
so in the code: 

arduino = serial.Serial(
'/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_0353638323635141C072-if00',
9600,
timeout=1
)

SPOON
usb-Arduino__www.arduino.cc__0043_0353637333235190F161-if00

so in the code

arduino = serial.Serial(
'/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_0353637333235190F161-if00',
9600,
timeout=1
)

python code to know the device index

import sounddevice as sd

print(sd.query_devices())

lets control the raspberrypi without desktop, mouse, keyboard, and run from my laptop with ssh , both connected to
my phone hotspot.
on raspi, run to check if ssh is active

sudo systemctl status ssh

if yes, on windows power shell run

ssh pc@elena.local


if it doesnt work, do

hostname -I

on the raspberrypi, and on the laptop run

ssh pc@IP_ADDRESS


ARDUINO CLI ON RASPBERRYPI
cd ~/Desktop/family/robot3/catapult-arduino-elena/
arduino-cli compile --fqbn arduino:avr:uno catapult-arduino-elena.ino
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno

VIDEO TEST

v4l2-ctl --list-devices
killall libcamera-hello
killall ffplay