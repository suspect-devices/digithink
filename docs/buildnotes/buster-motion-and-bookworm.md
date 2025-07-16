# Install motion on raspberry pi running debian bookworm
## install the base os.
## install the temperature monitor
```sh
ssh-keygen
nano .ssh/authorized_keys
nano ~-root/.ssh/authorized_keys
nano ~root/.ssh/authorized_keys
raspi-config
... Enable spi,i2c,text console, no splash, expand filesystem ...
reboot
apt install -y git-core
cd /usr/local/
git clone git@github.com:feurig/merlot.git
i2cdetect 1
i2cdetect 2
i2cdetect 0
cd merlot/
ls
pip3 install -r requirements.txt --break-system-packages
apt install -y prometheus-node-exporter
bin/readtemp.py
```
## Install motion.

Install and check the status of the motion service

```sh
wget https://github.com/Motion-Project/motion/releases/download/release-4.6.0/pi_bookworm_motion_4.6.0-1_arm64.deb
dpkg -i pi_bookworm_motion_4.6.0-1_arm64.deb
apt --fix-broken install
systemctl status motion
```

Make sure the camera works and adjust firmware config based on what libcamera has to say about it.

```sh
libcamera-vid -t 20000 libcamera-vid --codec libav -o test.mp4
rpicam-still -v -o test.jpg
rpicam-vid -t 10s --codec libav -o test.mp4
nano /boot/firmware/config.txt
...
dtoverlay=ov5647
...
reboot
```

Check that the camera still works (also check motion service)

```sh
rpicam-vid -t 10s --codec libav -o test.mp4
rpicam-hello
systemctl status motion
```

Install libcamerify and edit the motion.service definition.

```sh
apt install libcamera-tools libcamera-dev libcamera-v4l2 libcamerify
nano /lib/systemd/system/motion.service
...
[Service]
User=motion
UMask=002
EnvironmentFile=-/etc/default/motion
#ExecStart=/usr/bin/motion
ExecStart=/usr/bin/libcamerify /usr/bin/motion
...
systemctl restart motion
systemctl daemon-reload
systemctl restart motion
systemctl status motion
```

Make the system allow remote connections and fix location for output.

```sh
nano /etc/motion/motion.conf
...
# Target directory for pictures, snapshots and movies
target_dir /var/lib/motion
...
# Restrict webcontrol connections to the localhost.
webcontrol_localhost off
...
# Restrict stream connections to the localhost.
stream_localhost off
...
^X
systemctl restart motion
systemctl status motion
netstat -tunlp
```

Probably want to put mount /var/lib/motion on a fileserver.

```sh
mount utah:/tank/motion/buster /var/lib/motion
grep motion /etc/mtab>>/etc/fstab
mount -a
```

## References

- <https://forums.raspberrypi.com/viewtopic.php?t=359023>
- <https://pimylifeup.com/raspberry-pi-webcam-server/>
- <https://github.com/Motion-Project/motion/discussions/1753>
- <https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started>
