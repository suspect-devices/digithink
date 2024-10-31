# Debian install on kh2024

Currently just the bones
You are here fleshing this in.
Bouncing prompt is at.

<https://www.debian.org/releases/stable/amd64/apds03.en.html>

```sh
parted /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) p
Model: ATA TEAM T2532TB (scsi)
Disk /dev/sdb: 2048GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name  Flags
 1      1049kB  200GB   200GB   ext4         /
 2      200GB   201GB   1000MB  fat32        2     boot, esp
 3      201GB   2048GB  1847GB  ext4         3

(parted) rm 3
(parted) mkpart 3 ext3 201GB 501GB
(parted) p
Model: ATA TEAM T2532TB (scsi)
Disk /dev/sdb: 2048GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End    Size    File system  Name  Flags
 1      1049kB  200GB  200GB   ext4         /
 2      200GB   201GB  1000MB  fat32        2     boot, esp
 3      201GB   501GB  300GB   ext2         3

(parted) mkpart 4 linux-swap 501GB 600GB
(parted) mkpart 5 ext4 600GB 100%
(parted) print
Model: ATA TEAM T2532TB (scsi)
Disk /dev/sdb: 2048GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name  Flags
 1      1049kB  200GB   200GB   ext4         /
 2      200GB   201GB   1000MB  fat32        2     boot, esp
 3      201GB   501GB   300GB   ext4         3
 4      501GB   600GB   99.0GB               4     swap
 5      600GB   2048GB  1448GB  ext4         5

(parted) q
Information: You may need to update /etc/fstab.
```

set up mounts for chroot.

```sh
mkdir /mnt/debinst
mount /dev/sdb3 /mnt/debinst
mount -t proc proc /mnt/debinst/proc
mount -t sysfs /sys /mnt/debinst/sys
mount --bind /dev /mnt/debinst/dev
mount --bind /dev/pts /mnt/debinst/dev/pts
LANG=C.UTF-8 chroot /mnt/debinst /bin/bash
```

back on the chroot

```sh
.... second stage may not be needed ....
/debootstrap/debootstrap --second-stage
apt install makedev
cd /dev
MAKEDEV generic
nano /etc/fstab
mount -a
nano /etc/adjtime
dpkg-reconfigure tzdata
ip a
nano /etc/network/interfaces
nano /etc/resolv.conf
echo kh2024>/etc/hostname
nano /etc/hosts
apt install locales
dpkg-reconfigure locales
apt install grub2
... not sure about this one ...
grub install /dev/sdb
mount -a
apt install linux-image-amd64
apt install grub2
grub-update
grub-install /sdb
grub2-install /sdb
nano /etc/default/grub

update-grub2
```

make sure we can log into the box

```sh
apt install openssh-server
nano /etc/ssh/sshd_config
... disable root ssh login with password ...
adduser joe
adduser feurig
vigr
apt install sudo
visudo
passwd -u root
passwd root
nano ~root/.ssh/authorized_keys
```

copy the entire /etc/ssh/ directory so the host keys dont change

```sh
exit
cp -rpv /etc/ssh /mnt/debinst/etc/
LANG=C.UTF-8 chroot /mnt/debinst /bin/bash
```

Install gb ethernet firmware

```sh
nano /etc/apt/sources.list
apt update
apt install firmware-bnx2
update-grub
update-grub2
nano /etc/default/grub
reboot
```

Install zfs 2.2 from bookworm-backports

```sh
nano /etc/apt/sources.list
apt update
apt-get install linux-headers-$(uname -r)
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
zpool import -f tank
apt install parted
```

clean zfs info off of old devel and infra disk.

```sh
wipefs -a /dev/sde
```

```sh
nano /etc/sysctl.conf
...
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
...

sysctl net.ipv6.conf.all.disable_ipv6
```
