#kb2018 install bash history.
	df -k
	fdisk -l
	apt-get update&&apt-get dist-upgrade&& apt-get autoremove
	nano /etc/ssh/authorized_keys
	ssh bs2020
	ssh bs2020.suspectdevices.com
	ssh feurig@bs2020.suspectdevices.com
	scp feurig@bs2020.suspectdevices.com:steve.id .
	ls .ssh
	ls
	pwd
	exit
	apt-get update
	apt-get dist-upgrade
	apt-get install zfs*
	apt-get install bridgeutils
	apt-get install bridg*
	apt-get install nfs-kernel-server samba-common-bin zfs-initramfs zfs-dracut
	ip a
	ping archive.ubuntu.com
	apt-get install openssh-server
	service openssh-server status
	service openssh status
	service ssh status
	ip a
	su -feurig
	su - feurig
	nano /etc/default/grub
	update-grub
	nano /etc/default/grub
	nano /boot/grub/menu.lst
	nano /etc/netplan/50-cloud-init.yaml 
	ip a
	nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
	nano /etc/netplan/50-cloud-init.yaml 
	nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
	ip a
	nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
	nano /etc/netplan/50-cloud-init.yaml 
	netplan apply
	nano /etc/netplan/50-cloud-init.yaml 
	netplan apply
	df -k
	fdisk -l
	ip a
	ps -ef
	echo FUCKOFF> /dev/ttyS1
	reboot
	lxd --version
	vipw
	vigr
	useradd -help
	useradd -u 1001 -g 1001 -Gwheel,adm,sudo,plugdev,root -m joe -C "Joe Dumoulin" 
	vigr
	useradd -u 1001 -g 1001 -Gwheel,adm,sudo,plugdev,root -m joe -C "Joe Dumoulin" 
	useradd -u 1001 -g 1001 -Gadm,sudo,plugdev,root -m joe -C "Joe Dumoulin" 
	useradd -u 1001 -g 1001 -Gadm,sudo,plugdev,root -m -C "Joe Dumoulin"  joe
	useradd -u 1001 -g 1001 -Gadm,sudo,plugdev,root -m -c "Joe Dumoulin"  joe
	su - joe
	vipw -s
	vipw
	ls
	su - joe
	reboot
	last
	fdisk -l
	reboot
	fdisk -l
	reboot
	fdisk -l
	fdisk -l|grep Disk
	fdisk -l|grep Disk\ 
	fdisk -l|grep Disk\ \/
	fdisk /dev/sda
	apt-get install golang
	nano /etc/netplan/50-cloud-init.yaml 
	netplan apply
	nano /etc/netplan/50-cloud-init.yaml 
	netplan apply
	ip a
	nano /etc/netplan/50-cloud-init.yaml 
	netplan apply
	ip a
	fdisk -l
	parted /dev/sdb 
	fdisk -l
	lxd-init
	lxd init
	zfs list
	ls
	ps -ef
	ip a
	ls
	cat bs2020root.id>> /etc/ssh/authorized_keys.save 
	nano /etc/ssh/authorized_keys.save 
	cat ~root/.ssh/authorized_keys 
	cat bs2020root.id>> ~root/.ssh/authorized_keys 
	tail /var/log/syslog
	lxd profile show
	lxc profile show
	lxc profile show default
	ls
	lxc profile edit default
	cat susdev.yaml 
	lxc profile edit default
	lxc image list
	lxc image info
	lxc image list ubuntu:*
	lxc image alias list ubuntu:*
	lxc image alias list ubuntu:* 18.04
	lxc image alias list ubuntu:*server* 18.04
	lxc image copy ubuntu:18.04 local: --alias ubuntu-lts
	lxc launch ubuntu-lts guenter
	lxc list
	lxc attach guenter
	lxc attach exec guenter bash
	lxc  exec guenter bash
	lxc list
	ping 192.202.31.134
	ip a
	lxc  exec guenter bash
	brctl show
	lxc  exec guenter bash
	nano /etc/sysctl.conf 
	sysctl -p
	lxc  exec guenter bash
	reboot
	apt-get update&&apt-get dist-upgrade
	fdisk -l
	ls
	cat joes.keys 
	ls
	cat ~joe/.ssh/authorized_keys 
	last|less
	ls
	zfs list
	clear
	zfs list
	lxc list
	networkctl list
	nano /etc/netplan/50-cloud-init.yaml 
	netplan generate
	netplan apply
	networkctl list
	ip a
	up br0 up
	ip br0 up
	ip link br0 up
	ip a
	ifconfig br0 up
	ip a
	lxc lit
	lxc list
	lxc stop guenter
	lxc list
	ip a
	ifconfig br1 up
	lxc start guenter
	ip a
	lxc info guenter
	lxc exec guenter bash
	ps -ef
	lxc list
	nano /etc/systemd/network/br1.network
	nano /etc/systemd/network/br0.network
	reboot
	ls
	lxc list
	zpool status
	df -k
	ip a
	lxc shutdown guenter
	lxc stop guenter
	lxc edit guenter
	lxc help
	lxc config edit guenter
	lxc profile copy default
	lxc profile copy default infra
	lxc edit profile infra
	lxc profile edit infra
	lxc delete guenter
	networkctl list
	nano /etc/netplan/50-cloud-init.yaml 
	lxc create ubuntults guenter -p infra
	lxc launch ubuntults guenter -p infra
	lxc init local:ubuntults  guenter -p infra
	lxc image list
	lxc init local:ubuntu-lts  guenter -p infra
	lxc list 
	lxc exec guenter bash
	lxc start guenter bash
	lxc start guenter 
	lxc exec guenter bash
	lxc list 
	lxc exec guenter bash
	lxc list 
	lxc image list images:
	grep debian
	lxc image list images:|grep debian
	lxc image list debian:
	lxc image remote
	lxc image list
	lxc image list images:|grep centos
	lxc image list images:|grep redhat
	lxc image list images:|grep fedora
	lxc image list images:|grep suse
	lxc list
	ps -ef
	zfs list
	lxc profile edit default
	lxc profile show default
	lxd init
	fdisk -l
	zpool list
	zpool status
	lxd init
	zpool status
	lxc list
	lxd profile edit default
	lxc profile edit default
	lxc profile edit infra
	ls
	lxc image list
	lxc init ubuntu-lts larry 
	lxc start larry
	lxc list
	zpool status
	lxc init ubuntu-lts douglas
	lxc stop larry
	lxc delete larry
	lxc start douglass
	lxc start douglas
	lxc exec douglas bash
	lxc list
	clear
	ip a
	lxc config set core.https_address 192.168.31.159:8443
	lxc config set core.trust_password w3r3n3t$
	lxc remote add kb2018 192.168.31.159
	lxc remote list
	lxc remote remove kb2018
	lxc remote list
	lxc profile list
	lxc profile copy default susdev
	lxc profile list
	lxc list
	lxc start harvey
	lxc exec harvey bash
	lxc list
	lxc destroy harvey
	lxc stop harvey
	lxc delete harvey
	lxc list
	apt-get install htop
	htop
	ps -ef
	df -k
	lxc list
	zfs list
	lxc delete harvey
	zfs list
	lxc profile delete susdev
	lxc profile list
	lxc profile copy infra susdev
	lxc profile list
	lxc info teddy
	zfs list
	lxc profile delete susdev
	lxc start teddy
	lxc list
	dig digithink.com @dns2.digithink.com
	dig digithink.com @dns1.digithink.com
	lxc profile rename susdev
	lxc profile rename susdev susinfra
	lxc info teddy
	lxc profile copy default susdev
	lxc list
	lxc start sandbox 
	lxc list
	lxc info sandbox
	lxc exec sandbox bash
	lxc list
	ls
	lxc list
	lxc file put tracback.tgz douglas/home/feurig/
	lxc file push tracback.tgz douglas/home/feurig/
	lxc exec douglas bash
	apt-get update&& apt-get dist-upgrade&& apt-get autoremove
	ls
	lxc list 
	lxc start ian
	lxc list
	lxc start ernest
	lxc profile copy default susdev18.04
	lxc list
	lxc start kurt
	lxc list
	lxc start morgan
	lxc list
	lxc delete oldtrac
	lxc list
	lxc start oldtrac 
	lxc phillip
	lxc start phillip
	lxc list
	lxc start harvey
	lxc delete harvey
	reboot
	lxc list
	lxc info phillip
	lxc init local:utbunt-lts sarina
	lxc init local:utbuntu-lts sarina --profile=infra
	lxc list profile
	lxc profile list
	zpool list
	lxc stop guenter
	ls /var/lib/lxd/storage-pools/infra/containers/guenter/
	lxc start guenter
	ls /var/lib/lxd/storage-pools/infra/containers/guenter/
	lxc help
	lxc storage help
	lxc storage show
	lxc storage show infra
	lxc help
	ls
	lxc list
	lxc start naomi 
	lxc put naomiroot.tgz naomi:/home/feurig/
	lxc file put naomiroot.tgz naomi:/home/feurig/
	lxc file push naomiroot.tgz naomi:/home/feurig/
	lxc file push naomiroot.tgz naomi/home/feurig/
	lxc exec naomi bash
	tar -xzvf  naomiroot.tgz 
	pwd
	ls
	cd var/lib/lxc/naomi/
	ls -ls
	ls rootfs/etc/
	ls -ls rootfs/etc/
	df -k
	ls /var/lib/lxd/storage-pools/infra/containers/naomi/
	mv /var/lib/lxd/storage-pools/infra/containers/naomi/rootfs /var/lib/lxd/storage-pools/infra/cont
	mv rootfs /var/lib/lxd/storage-pools/infra/containers/naomi/
	lxc list
	lxc help
	lxc exec naomi bash
	ls
	lxc list
	lxc exec naomi bash
	lxc config set naomi  security.privileged true
	lxc exec naomi bash
	lxc list
	fdisk -l
	cd /srv/installmedia/
	ls
	wget https://downloads.sourceforge.net/gparted/gparted-live-0.32.0-1-amd64.iso
	wget
	wget https://download.fedoraproject.org/pub/fedora/linux/releases/28/Server/x86_64/iso/Fedora-Ser
	ls
	wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-9.5.0-amd64-netinst.iso
	ls
	wget https://saimei.ftp.acc.umu.se/debian-cd/current/amd64/iso-dvd/debian-9.5.0-amd64-DVD-2.iso
	ip a
	apt get install samba samba-common-bin
	apt-get install samba samba-common-bin
	mkdir /srv/installmedia
	cd /srv/installmedia/
	wget http://releases.ubuntu.com/18.04.1/ubuntu-18.04.1-live-server-amd64.iso?_ga=2.217616086.1525
	apt-get remove samba
	apt-get autoremove
	ls
	mv ubuntu-18.04.1-live-server-amd64.iso\?_ga\=2.217616086.1525765299.1538535940-781929701.1526740
	ls
	apt-get install nfs-kernel-server
	ls -ls
	nano /etc/exports 
	exportfs -a
	nano /etc/exports 
	exportfs -a
	showmount -e
	useradd -c"nfs client"  nfs
	passwd nfs
	ls
	ip a
	tail /var/log/syslog
	tail -f /var/log/syslog
	nano /etc/exports 
	exportfs -a
	showmount -e
	ls -ls /srv/installmedia/ubuntu-18.04.1-live-server-amd64.iso
	showmount -e
	passwd nfs
	su - feurig
	vipw
	su - feurig
	ls 
	showmount -e
	ip -a
	ip a
	showmount -e
	ufw
	ufw help
	ufw status
	showmount -e
	nano /etc/exports 
	ls
	chown -R nfs /srv/installmedia
	ls -ls
	wget https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/debian-9.5.0-amd64-DVD-1.iso
	ls
	arp -a
	ssh feurig@192.168.31.200
	ssh feurig@192.168.31.158
	ls
	cd /srv/installmedia/
	ls
	cd /srv/installmedia/
	ls
	ls -ls
	userdel nfs
	ls
	ls-ls
	ls -ls
	chown root *
	ls -ls
	ls
	arp -a
	ping 192.168.31.196
	ping 192.168.31.200
	ssh feurig@192.168.31.200
	ping 192.168.31.158
	ssh feurig@192.168.31.158
	
