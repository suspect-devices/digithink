# tk2022 -- Rebuild kb2018 using debian bookworm.

The process for installing debian on the old dl380 is about the same as the dell excep that its bios and not uefi and the disks have to be set up by the controller. (flesh this in a bit)
## Prep

For reference see [Build notes for guthrie](/buildnotes/guthrie/)

- back up all containers to /tank
- convert all lxd containers to incus with lxd-to-incus
- migrate all incus containers to temporary server

## Rebuild

### Partition the disk 

```sh
parted /dev/sdg
GNU Parted 3.6
Using /dev/sdg
...mkpart until you get the stuff below....
(parted) print
Model: HP LOGICAL VOLUME (scsi)
Disk /dev/sdg: 1024GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: pmbr_boot

Number  Start   End     Size    File system  Name   Flags
 1      1049kB  2097kB  1049kB  fat32                 bios_grub
 2      2097kB  250GB   250GB   ext4
 3      250GB   500GB   250GB   ext4         incus

(parted)disk_set pmbr_boot on
(parted)set 1 bios_grub on
(parted)quit
```
Create the root filesystem. You can save yourself some time by copying down the UUID for later.

```
mkfs.ext4 -j /dev/sdg2
mount /dev/sdg2 /mnt/tktest/
```

apt install debootstrap
```

### Debootstrap with proxy.

```sh
export http_proxy=http://192.168.31.2:3128/
debootstrap --arch amd64 bookworm /mnt/debinst http://ftp.us.debian.org/debian
```

### Grab a few things from the old server.

```sh
mkdir /mnt/tktest
mount /dev/sdj /mnt/tktest
incus admin init --dump>/mnt/tktest/root/incusinit.yml
cp -rpv /etc/ssh /mnt/tktest/etc/
cp -rpv /root/.ssh /mnt/tktest/root/
```

### Mount chroot environment.
```
mount -t sysfs /proc /mnt/tktest/proc
mount -t sysfs /sys /mnt/tktest/sys
mount --bind /dev /mnt/tktest/dev
mount --bind /dev/pts /mnt/tktest/dev/pts
LANG=C.UTF-8 chroot /mnt/tktest /bin/bash
```

#### Alternate way to mount

```sh
mkdir /mnt/tktest
mount /dev/sdj /mnt/tktest
mount --make-rslave --rbind /proc /mnt/tktest/proc
mount --make-rslave --rbind /sys /mnt/tktest/sys
mount --make-rslave --rbind /dev /mnt/tktest/dev
mount --make-rslave --rbind /dev/pts /mnt/tktest/dev/pts
LANG=C.UTF-8 chroot /mnt/tktest /bin/bash
PS1='TKTEST\w\$ '
```

### Set up apt (with proxy) (UPDATED T0 REFLECT 2025 HPE REPO LOCATION)

Get the signing keys for hpe repos (needed later for ssacli).

```sh
export https_proxy=http://192.168.31.2:3128/
curl https://downloads.linux.hpe.com/SDR/hpPublicKey2048_key1.pub | gpg --dearmor | sudo tee -a /usr/share/keyrings/hpePublicKey.gpg > /dev/null
curl https://downloads.linux.hpe.com/SDR/hpePublicKey2048_key1.pub | gpg --dearmor | sudo tee -a /usr/share/keyrings/hpePublicKey.gpg > /dev/null
curl https://downloads.linux.hpe.com/SDR/hpePublicKey2048_key2.pub | gpg --dearmor | sudo tee -a /usr/share/keyrings/hpePublicKey.gpg > /dev/null
```

Update repos to include backports (needed to get the right zfs version) and hpe (needed for ssacli).

```sh
cat >/etc/apt/sources.list<<EOD
#deb http://ftp.us.debian.org/debian bookworm main
deb http://deb.debian.org/debian bookworm main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-updates main non-free non-free-firmware contrib
deb http://deb.debian.org/debian-security/ bookworm-security main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
# deb [trusted=yes] http://downloads.linux.hpe.com/SDR/downloads/MCP/debian bookworm/current non-free 
deb [signed-by=/usr/share/keyrings/hpePublicKey.gpg] https://downloads.linux.hpe.com/SDR/repo/mcp/debian bookworm/current non-free

Tell apt to use the admin lans http(s) proxy. 

EOD
TKTEST/# cat > /etc/apt/apt.conf.d/99proxy <<EOD
> Acquire::http::Proxy "http://192.168.31.2:3128/";
> EOD
```


### Set up the fstab.
We want to use the uuid for the mounts. *The hp raid controller shuffles the /dev/sdx quite a bit.*
```
blkid|grep sdb|sed 's/^/# /' >>/etc/fstab
nano /etc/fstab
UUID=c51cb56b-9da4-479b-ba11-dfaac580df64 / ext4 rw,relatime 0 0
UUID=5456b1ce-999f-43a1-b13f-d507321f3ed8 /var/lib/incus ext4 rw,relatime 0 0
# /dev/sdb2: UUID="c51cb56b-9da4-479b-ba11-dfaac580df64" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="ad01a32f-edc1-4f85-a8e3-b27b2e92fd03"
# /dev/sdb3: UUID="5456b1ce-999f-43a1-b13f-d507321f3ed8" BLOCK_SIZE="4096" TYPE="ext4" PARTLABEL="incus" PARTUUID="998a853e-da55-453a-a936-65d559454ef7"
# /dev/sdb1: PARTUUID="ce1294c5-8fb4-4c82-a3ea-40b6f9872efd"

```

### Install stuff you will want installed.

```sh
apt install openssh-server
apt install ca-certificates
apt install curl
apt install gpg
apt install sudo
apt install parted
apt install htop
apt install git
apt install ssacli
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
Make sure you install bridge-utils otherwise the bridges wont come up.
```
apt install bridge-utils 
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

This is kind of silly since you need to proxy to get anywhere and the proxies do dns. However we do want resolution for the admin land so we add sitka and naomis internal address. 

```sh
cat >/etc/resolv.conf<<EOD
192.168.31.2             # sitka (dnsmasq)
192.168.31.141           # naomi's internal address
search admin.suspectdevices.com merlot.suspectdevices.com suspectdevices.com digithink.com fromhell.com
EOD
```

### Install the gigabyte nic drivers.
A linux box without network is secure but useless.
```sh
apt update
apt install firmware-bnx2
```

### Update grub
Since the hp is bios based we install grub-pc rather than an efi based solution.

```sh
apt install grub-pc
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
### Add update script.

```sh
nano /usr/local/bin/update.sh
#!/bin/bash
# update.sh for debian/ubuntu/centos/suse  (copyleft) don@suspecdevices.com
echo --------------------- begin updating `uname -n` ----------------------
if [ -x "$(command -v apt-get)" ]; then
   apt-get update
   apt-get -y dist-upgrade
   apt-get -y autoremove
fi
if  [ -x "$(command -v yum)" ]; then
   echo yum upgrade.
   yum -y upgrade
fi
if  [ -x "$(command -v zypper)" ]; then
   echo zypper dist-upgrade.
   zypper -y dist-upgrade
fi
echo ========================== done ==============================
^X
chmod +x /usr/local/bin/update.sh
```
### Install ssacli

```
apt update
apt install ssacli
```

### Using ssacli to set the primary boot disk.

```sh
=> set target ctrl slot=0

   "controller slot=0"

=> show config detail
... find the drive that coresponds to what you want

=> ld 10 modify bootvolume=primary
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

### Install zfs from trixie

The version of zfs installed by bookworm is behind the one that the zabbly incus install wants so we go to trixies backport. 

```sh
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
```

### Install incus from zabbly (with proxy)


```sh
apt install curl
curl  -x http://192.168.31.2:3128/ -fsSL https://pkgs.zabbly.com/key.asc -o /etc/apt/keyrings/zabbly.asc
sh -c 'cat <<EOF > /etc/apt/sources.list.d/zabbly-incus-stable.sources
Enabled: yes
Types: deb
URIs: https://pkgs.zabbly.com/incus/stable
Suites: $(. /etc/os-release && echo ${VERSION_CODENAME})
Components: main
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/zabbly.asc

EOF'
apt update
apt install incus
incus admin init

incus storage create devel zfs source=/dev/disk/by-id/wwn-0x600508b1001cfe22c14c918541d42c3a-part1 zfs.pool_name=devel
ls -ls /dev/disk/by-id|grep sda
zpool status devel
zpool attach devel wwn-0x600508b1001cfe22c14c918541d42c3a-part1 wwn-0x600508b1001c2ad6bd48a76e9aee8e03-part1
zpool status infra
zpool attach infra wwn-0x600508b1001cfe22c14c918541d42c3a-part2 wwn-0x600508b1001c2ad6bd48a76e9aee8e03-part2
```

### Migrate containers back from spare server.

Again see [Build notes for guthrie](/buildnotes/guthrie/)


### Install ansible and set up bitbicket repository

Create an access key on bitbucket with write access to the SusdevAdmin/ansible repo. 

Copy the key somewhere safe.

```sh
git config --global http.proxy http://192.168.31.2:3128
git clone https://x-token-auth:<Token from above>@bitbucket.org/suspectdevicesadmin/ansible.git
ls
cd ansible/
ls
nano ansible.cfg
nano hosts
git config user.email <username provided above>@bots.bitbucket.org
git commit -a -m"test through proxy"
git push
```



## References.
- https://www.debian.org/releases/stable/amd64/apds03.en.html
- https://downloads.linux.hpe.com/SDR/downloads/MCP/debian/dists/bookworm/
- https://sleeplessbeastie.eu/2017/06/26/how-to-fix-the-missing-hpes-public-keys/
- https://serverfault.com/questions/1142235/-debian-12-live-grub-installerror-boot-efi-doesnt-look-like-an-efi-partition
- https://linuxopsys.com/mount-partitions-using-uuid-in-linux
-https://www.cyberciti.biz/faq/linux-finding-using-uuids-to-update-fstab/
