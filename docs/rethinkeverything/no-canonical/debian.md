```Using /dev/sdb
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

(parted) help
  align-check TYPE N                       check partition N for TYPE(min|opt) alignment
  help [COMMAND]                           print general help, or help on COMMAND
  mklabel,mktable LABEL-TYPE               create a new disklabel (partition table)
  mkpart PART-TYPE [FS-TYPE] START END     make a partition
  name NUMBER NAME                         name partition NUMBER as NAME
  print [devices|free|list,all]            display the partition table, or available devices, or free space, or all found partitions
  quit                                     exit program
  rescue START END                         rescue a lost partition near START and END
  resizepart NUMBER END                    resize partition NUMBER
  rm NUMBER                                delete partition NUMBER
  select DEVICE                            choose the device to edit
  disk_set FLAG STATE                      change the FLAG on selected device
  disk_toggle [FLAG]                       toggle the state of FLAG on selected device
  set NUMBER FLAG STATE                    change the FLAG on partition NUMBER
  toggle [NUMBER [FLAG]]                   toggle the state of FLAG on partition NUMBER
  type NUMBER TYPE-ID or TYPE-UUID         type set TYPE-ID or TYPE-UUID of partition NUMBER
  unit UNIT                                set the default unit to UNIT
  version                                  display the version number and copyright information of GNU Parted
(parted) rm 3
(parted) mkpart 3 primary 201GB 501GB
parted: invalid token: primary
File system type?  [ext2]?
Start? 201GB
End? 501GB
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

(parted) mkpart 4
File system type?  [ext2]? swap
parted: invalid token: swap
File system type?  [ext2]? ?
parted: invalid token: ?
File system type?  [ext2]? linux-swap
Start? 501GB
End? 600GB
(parted) mkpart 5
File system type?  [ext2]? hidden
parted: invalid token: hidden
File system type?  [ext2]? ext4
Start? 600GB
End? 100%
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
```
mount /dev/sdb3 /mnt/debinst
mount -t proc proc /mnt/debinst/proc
mount -t sysfs /sys /mnt/debinst/sys
mount --bind /dev /mnt/debinst/dev
mount --bind /dev/pts /mnt/debinst/dev/pts
LANG=C.UTF-8 chroot /mnt/debinst /bin/bash
```
back on the chroot
```
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
nano /etc/network/interfaces
nano /etc/resolv.conf
echo kh2024>/etc/hostname
nano /etc/hosts
apt install locales
dpkg-reconfigure locales
apt install grub-pc
grub install /dev/sdb
grub-install /dev/sdb
exit
apt install console-setup
mount -a
apt search linux-image
apt install linux-image
apt install linux-image-amd64
apt install grub2
grub-update
grub-install /sdb
grub2-install /sdb
nano /etc/default/grub
update-grub2
```
make sure we can log into the box
```
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
Install gb ethernet firmware
```
nano /etc/apt/sources.list
apt update
apt install firmware-bnx2
update-grub
update-grub2
nano /etc/default/grub
reboot
```
Install zfs 2.2 from bookworm-backports
```
nano /etc/apt/sources.list
apt update
apt-get install linux-headers-$(uname -r)
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
zpool import -f tank
apt install parted
```
clean zfs info off of old devel and infra disk.
```
wipefs -a /dev/sde
```

```
nano /etc/sysctl.conf
...
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
...

sysctl net.ipv6.conf.all.disable_ipv6
```
