# tk2022 -- Rebuild kb2018 using debian bookworm.
## ----------------------- ROUGH IN --------------------------

Ok. So ubuntu let me install on the old HP dl-380 with its funky raid controller and bios. (no uefi). I have not been able thus far to 

### Partition the disk (this needed to be redone)
Add a section for cloning working partition table with sgdisk

```sh
parted /dev/sdg
GNU Parted 3.6
Using /dev/sdg
...
(parted) print
Model: HP LOGICAL VOLUME (scsi)
Disk /dev/sdg: 1024GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system     Name  Flags
 1      1049kB  1048MB  1046MB  fat32           boot  msftdata
 2      1048MB  2048MB  1000MB  linux-swap(v1)  swap  swap
 3      2048MB  300GB   298GB   ext4            root
 4      300GB   1024GB  724GB   zfs             free
quit
mkfs.ext4 -j /dev/sdg3
mount /dev/sdg3 /mnt/debinst/
apt install debootstrap
```

### Debootstrap with proxy.

```sh
export http_proxy=http://192.168.31.2:3128/
debootstrap --arch amd64 bookworm /mnt/debinst http://ftp.us.debian.org/debian
```

### Mount chroot environment.

```sh
mkdir /mnt/tktest
mount -t sysfs /proc /mnt/tktest/proc
mount -t sysfs /sys /mnt/tktest/sys
mount --bind /dev /mnt/tktest/dev
mount --bind /dev/pts /mnt/tktest/dev/pts
LANG=C.UTF-8 chroot /mnt/tktest /bin/bash

```

#### Alternate way to mount

```sh
mount --make-rslave --rbind /proc /mnt/tktest/proc
mount --make-rslave --rbind /sys /mnt/tktest/sys
mount --make-rslave --rbind /dev /mnt/tktest/dev
mount --make-rslave --rbind /dev/pts /mnt/tktest/dev/pts
LANG=C.UTF-8 chroot /mnt/tktest /bin/bash
PS1='TKTEST\w\$ '
```

### Set up apt

```sh
cat >/etc/apt/sources.list<<EOD
#deb http://ftp.us.debian.org/debian bookworm main
deb http://deb.debian.org/debian bookworm main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-updates main non-free non-free-firmware contrib
deb http://deb.debian.org/debian-security/ bookworm-security main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
deb [trusted=yes] http://downloads.linux.hpe.com/SDR/downloads/MCP/debian bookworm/current non-free # disabled on upgrade to focal

EOD
TKTEST/# cat > /etc/apt/apt.conf.d/99proxy <<EOD
> Acquire::http::Proxy "http://192.168.31.2:3128/";
> EOD
```

### Make devices

```sh
TKTEST/# apt install makedev
cd /dev
MAKEDEV generic
```

### Set up  time

There should be a way to preseed the time zone.

```
cat> /etc/adjtime<<EOD
0.0 0 0.0
0
UTC
EOD
dpkg-reconfigure tzdata
```

### Set up networking

```
cat >/etc/network/interfaces<<EOD
#-------------------------------------------------------------------/etc/network/interfaces
# 2: enp3s0f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br0 state UP group default qlen 1000
# 3: enp3s0f1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br1 state UP group default qlen 1000
# 4: enp4s0f0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
# 5: enp4s0f1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000 qdisc mq master br3 state UP group default qlen 1000
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

iface enp3s0f0 inet manual
iface enp3s0f1 inet manual
iface enp4s0f0 inet manual
iface enp4s0f1 inet manual

auto br0
iface br0 inet manual
     bridge_ports enp3s0f0
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay


auto br1
iface br1 inet static
     address 192.168.31.159
     network 192.168.31.0
     netmask 255.255.255.0
     broadcast 192.168.31.255
     bridge_ports enp4s0f1
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
EOD
```

### Set up resolution. 

This is kind of silly since you need to proxy to get anywhere and the proxies do dns. This should change to use sitka and an admin lan should be added. (proposed change below)

```sh
cat >/etc/resolv.conf<<EOD
192.168.31.2             # sitka (dnsmasq)
192.168.31.141           # naomi's internal address
search admin.suspectdevices.com merlot.suspectdevices.com suspectdevices.com digithink.com fromhell.com
EOD
```

### Install the gigabyte nic drivers.

```sh
apt update
apt install firmware-bnx2
```

### !!!! Investigate this !!!!. 

```sh
#   info -f grub -n 'Simple configuration'
```

### Update grub

This currently isnt working. 

```sh
nano /etc/default/grub
GRUB_TERMINAL=console serial
GRUB_GFXPAYLOAD_LINUX=text
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_SERIAL_COMMAND="serial --speed=115200"
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="console=tty1 console=ttyS1,115200n8 ipv6.disable=1 iommu=pt"
GRUB_CMDLINE_LINUX="console=tty1 console=ttyS1,115200n8 ipv6.disable=1 iommu=pt"
GRUB_DISABLE_OS_PROBER=false
grub-install /dev/sdj
update-grub2
```

### Install ssacli

```
apt install gpg
apt install curl
curl -x http://192.168.31.2:3128/ -fsSL https://downloads.linux.hpe.com/SDR/hpPublicKey2048.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpPublicKey2048.gpg
curl -x http://192.168.31.2:3128/ -fsSL https://downloads.linux.hpe.com/SDR/hpePublicKey2048_key1.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpePublicKey2048_key1.gpg
curl -x http://192.168.31.2:3128/-fsSL https://downloads.linux.hpe.com/SDR/hpPublicKey2048_key1.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpPublicKey2048_key1.gpg
apt update
apt install ssacli
```

### Using ssacli to set the primary boot disk.

```sh
=> set target ctrl slot=0

   "controller slot=0"

=> show config detail
... find the drive that coresponds to what you want

=> ld 1 modify bootvolume=primary
=>
```

###

To recover if the selected drive does not boot log into the ilo.

```sh
</>hpiLO-> power reset

status=0
status_tag=COMMAND COMPLETED
Thu Nov 28 17:04:30 2024

Server resetting .......

</>hpiLO-> vsp
```

Wait for the eternity it takes to run through the hardware and memory on the hp. Once it gets to the actual bios change to the text console.

```sh
<ESC>(
</>hpiLO-> textcons
```

The text console is nice because (inspite of char set differences) the function keys work. Press f8 when you get to the raid controller (after it searches for the disks)

Text console will not work until it actually gets to the bios and you can switch back to the VSP by escaping out 

```sh
<ESC>(
</>hpiLO-> vsp

Virtual Serial Port Active: COM2
```

## References.

- https://downloads.linux.hpe.com/SDR/downloads/MCP/debian/dists/bookworm/
- https://sleeplessbeastie.eu/2017/06/26/how-to-fix-the-missing-hpes-public-keys/
- https://serverfault.com/questions/1142235/-debian-12-live-grub-installerror-boot-efi-doesnt-look-like-an-efi-partition
- 