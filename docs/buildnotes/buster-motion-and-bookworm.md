### References

- <https://forums.raspberrypi.com/viewtopic.php?t=359023>
- <https://pimylifeup.com/raspberry-pi-webcam-server/>
- <https://github.com/Motion-Project/motion/discussions/1753>
- <https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started>

### Raw Dump of motion install

```sh
wget https://github.com/Motion-Project/motion/releases/download/release-4.6.0/pi_bookworm_motion_4.6.0-1_arm64.deb
dpkg -i pi_bookworm_motion_4.6.0-1_arm64.deb
apt --fix-broken install
systemctl status motion
libcamera-vid -t 20000 libcamera-vid --codec libav -o test.mp4
rpicam-still -v -o test.jpg
rpicam-vid -t 10s --codec libav -o test.mp4
nano /boot/firmware/config.txt
reboot
rpicam-vid -t 10s --codec libav -o test.mp4
rpicam-hello
motion --version
apt install libcamera-tools libcamera-dev libcamera-v4l2
libcamerify
nano /lib/systemd/system/motion.service
systemctl restart motion
systemctl daemon-reload
systemctl restart motion
systemctl status motion
netstat -tunlp
nano /etc/motion/motion.conf
systemctl restart motion
nano /etc/motion/motion.conf
ls -ls /etc/motion/
chown motion:adm motion.conf
chown motion:adm /etc/motion/motion.conf
chmod +w /etc/motion/motion.conf
systemctl restart motion
systemctl status motion
netstat -tunlp
mount utah:/tank/motion/buster /var/lib/motion
grep motion /etc/mtab>>/etc/fstab
mount -a
cat /etc/fstab
```
