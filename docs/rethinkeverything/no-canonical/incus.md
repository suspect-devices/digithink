```
apt -t bookworm-backports install incus incus-tools
apt install bridge-utils
ip a
nano /etc/network/interfaces
.... add bridge ...
systemctl restart networking
ip a
incus init
incus admin help
incus admin init
fdisk -l |grep -v loop|grep Disk
df -k
fdisk -l /dev/sdc
fdisk -l /dev/sdd
fdisk -l /dev/sdb
parted /dev/sdb
... split off a 300G partition for infra pool ...
ls -lsa /dev/disk/by-id/|grep sdb
... save this for infra partition device ...
incus admin init
incus image list images: bookworm
incus image copy images:debian/12/cloud local:
incus image copy images:debian/13/cloud local:
incus image list images: trixie
incus image copy images:debian/trixie/cloud local:
incus image list
incus alias add bookworm 4ed6d8b34c84
incus alias add trixie b0104c654d3d
incus image alias create bookworm 4ed6d8b34c84
incus image alias create trixie b0104c654d3d
incus image list
incus launch local:bookworm teddy -p default -p susdev24
incus list
incus exec teddy bash
cat /etc/sysctl.conf
incus exec teddy bash
```