# Replace ubuntu with debian on home server.
*Debian trixy install on utah repeat the process of installing debian on one of the home servers.*

Utah is my secondary home file server. It is a cheeze grater style mac with 2 matched 2t ssds on a pci card that are the boot disks and then mirrored 8T and 14T zfs disks. Like the other 2 home servers it is an appletalk server as well as providing lxc containers and running docker processes. 


On utah we have a 2t ssd that was intended to be the mirror disk for utah's zfs root disk. We partitioned it so that we have a boot, swap and root partition as well as 1.7T of free space.

```sh
parted /dev/sde print
Model: ATA TEAM T2532TB (scsi)
Disk /dev/sde: 2048GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name  Flags
 1      1049kB  583MB   582MB   ntfs         1     boot, esp
 2      583MB   2685MB  2102MB               2     swap
 3      2685MB  250GB   247GB   ext3         3
 4      250GB   2048GB  1798GB               4
```

So we start from here. 

```sh
apt install debootstrap
```

set up target root filesystem

```sh
mke2fs -j /dev/sde3
```
bootstrap the root file system

```sh
mkdir /mnt/debinst
mount /dev/sde3 /mnt/debinst
debootstrap --arch amd64 trixie /mnt/debinst http://ftp.us.debian.org/debian
```