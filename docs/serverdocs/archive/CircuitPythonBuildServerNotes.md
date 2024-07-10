# Building Circuit Python.

I was looking at adafruits circuit python as a possible platform fo replace the missing link using either the rpi2040 or the esp32s2. Unfortunately the usb stacks supported are different so I knew I would have to build what I want from scratch. I am not sure that this isnt a rathole.

[https://learn.adafruit.com/building-circuitpython/build-circuitpython](https://learn.adafruit.com/building-circuitpython/build-circuitpython)

### Building on Sandbox (ubuntu focal)
Circuitpython for most processors requires more than a few dependencies. 

```
sudo apt-get install build-essential git gettext uncrustify python3-pip
sudo apt-get install python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
sudo pip3 install cascadetoml
sudo apt-get install gcc-arm-none-eabi
```

This should allow you to check out the source code for circuitpython as a user. As per their suggestions I forked the repo first.

```
git clone git@github.com:suspect-devices/circuitpython.git
cd circuitpython/
git submodule sync --quiet --recursive
git submodule update --init
```
Once there you can install further dependencies.

```
sudo pip3 install -r requirements-dev.txt 
sudo make -C mpy-cross
```
At which point you can build firmware for most targets.

```
cd ports/raspberrypi/
make BOARD=adafruit_feather_rp2040
cd build-adafruit_feather_rp2040/
```
#### Adding the Espressif toolchain and idf

``` 
cd /home/feurig/circuitpython/ports/esp32s2# 
sudo esp-idf/install.sh 
```


### First attempt.
On my first attemp I was only interested in building for the esp32s2. I ran everything as root including the builds. It is better to separate privilages with anything this large where you are building for a different target. 

```
root@viva:# apt-get install git wget flex bison gperf python3 python3-pip python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
...
root@viva:/home/feurig# mkdir -p ~/esp
root@viva:/home/feurig# cd ~/esp
root@viva:~/esp# git clone --recursive https://github.com/espressif/esp-idf.git
Cloning into 'esp-idf'...
...
root@viva:~/esp# cd esp-idf/
root@viva:~/esp/esp-idf# ./install.sh 
...
All done! You can now run:

  . ./export.sh

root@viva:~/esp/esp-idf# . ./export.sh
...
root@viva:~# cd /home/feurig/circuitpython/
root@viva:/home/feurig/circuitpython# cd ports/
root@viva:/home/feurig/circuitpython/ports# cd esp32s2/
root@viva:/home/feurig/circuitpython/ports/esp32s2# make BOARD=unexpectedmaker_feathers2
...
Wrote 2601984 bytes to build-unexpectedmaker_feathers2/firmware.uf2
root@viva:/home/feurig/circuitpython/ports/esp32s2# 

```
Then as a comparison I built for the adafruit feather rp2040.

```
root@viva:/home/feurig/circuitpython/ports# cd raspberrypi/
root@viva:/home/feurig/circuitpython/ports/raspberrypi# ls boards/
adafruit_feather_rp2040    pimoroni_keybow2040  raspberry_pi_pico
adafruit_itsybitsy_rp2040  pimoroni_picosystem  sparkfun_pro_micro_rp2040
adafruit_qtpy_rp2040       pimoroni_tiny2040    sparkfun_thing_plus_rp2040
root@viva:/home/feurig/circuitpython/ports/raspberrypi# make BOARD=adafruit_feather_rp2040
Use make V=1, make V=2 or set BUILD_VERBOSE similarly in your environment to increase build verbosity.
QSTR updated
Traceback (most recent call last):
  File "gen_stage2.py", line 2, in <module>
    import cascadetoml
ModuleNotFoundError: No module named 'cascadetoml'
root@viva:/home/feurig/circuitpython/ports/raspberrypi# pip3 install cascadetoml
...
root@viva:/home/feurig/circuitpython/ports/raspberrypi# make BOARD=adafruit_feather_rp2040
...
Wrote 1259520 bytes to build-adafruit_feather_rp2040/firmware.uf2
root@viva:/home/feurig/circuitpython/ports/raspberrypi#  
```