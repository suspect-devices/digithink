<!-- BS2020InstallNotes, Version: 1, Modified: 2018/12/02, Author: trac -->

# BS2020 (RE)Install

NotesInstalling devstack on server left entirely too much shit everywhere. Realized that devstack should be installed in a container or vm. This page documents the reinstallation of bs2020 using the remote console and admin network.
## Firewall Setup
Allowing access to the server is discussed in the [wiki:OpenWRT OpenWRT notes] section.
## Loading a new os via the idrac 6

* log into idrac by browsing (https://vpn.suspectdevices.com)
* open the virtual console. (accept all responsibility for allowing it to run)
* launch virtual media 
* attach ubuntu 16.04 server iso (on your local workstation)
* boot the iso and install the server according to either the official server install instructions or your favorite i.e. https://ittutorials.net/linux/ubuntu/install-ubuntu-16-04-lts/
  * While booting adjust the bios settings to skip PXE booting and memory testing which takes for ever
  * Let the vpn on the admin lan provide the address and network settings on the first interface (will fix later)
  * Select ssh server (dns,lamp, and mail will be handled by containers anything else will be faster over the net)
* ssh into box once the os is installed.

## Post install configuration

Make primary interface static (on admin lan)
```sh
root@bs2020:~# nano /etc/network/interfaces
...
# The primary network interface
auto eno1
iface eno1 inet static
	address 192.168.1.158/24
	gateway 192.168.1.1
	dns-nameservers 192.168.1.1 198.202.31.132 198.202.31.141
	dns-search vpn suspectdevices.com digithink.com 
...
root@bs2020:~#

Update server

feurig@bs2020:~$ sudo bash
[sudo] password for feurig: 
root@bs2020:~# apt-get update
... Done
root@bs2020:~# apt-get dist-upgrade
root@bs2020:~# apt-get install openssl-server


Add second admin user

root@bs2020:~# useradd -m joe -c"Joe Dumoulin" -Gsudo,root
root@bs2020:~# su - joe
joe@bs2020:~$ nano
joe@bs2020:~$ mkdir .ssh
joe@bs2020:~$ nano .ssh/authorized_keys
```	
  _paste key from vpn /etc/dropbear/autorized_keys_

Set initial password so that admin can sudo.
	
	root@bs2020:~# vipw -s
	... paste hash from medea ...
	
Consider removing password based ssh authentication once both admins can connect.

## LXC

_ This should probably move to its own section once stable _

We want to do 3 things with lxc.
* create a public facing server for dns/email/and other services which is isolated from other containers and can not access the host directly
* create a similarly isolated server for openstack/devstack that can be uninstalled and which will not shit all over everything. (Attempting to containerize devstack was as disastrous as trying to uninstall it)
* create user space containers for experimentation which are in themselves isolated from everything else.

### LXC and the first infrastructure container
Lxd is installed but lxc is not. Install lxc lxc templates bridge utilities and zfs. 
In the example below we leverage lxd to create the zfs pool and to point the lxc network to the the existing bridge. Once we work enough with LXC/LXD and zfs to identify the relative merits of each approach I will backfill how to do these tasks manually.

	
```	root@bs2020:~# sudo apt-get install lxc  lxc-templates wget \
						zfsutils-linux bridge-utils  ebtables openvswitch-common
...
root@bs2020:~# nano /etc/network/interfaces

# The primary network interface
auto eno1
iface eno1 inet static
	address 192.168.1.158/24
	gateway 192.168.1.1
	dns-nameservers 192.168.1.1 198.202.31.132 198.202.31.141
	dns-search vpn suspectdevices.com digithink.com

auto br0
iface br0 inet static
	address 0.0.0.0
	bridge_ports eno4  

iface eno4 inet manual

...
root@bs2020:~# lxd init
Name of the storage backend to use (dir or zfs) [default=zfs]: 
Create a new ZFS pool (yes/no) [default=yes]? yes
Name of the new ZFS pool [default=lxd]: lxd4infra
Would you like to use an existing block device (yes/no) [default=no]? yes
Path to the existing block device: /dev/sde1
Would you like LXD to be available over the network (yes/no) [default=no]? 
Do you want to configure the LXD bridge (yes/no) [default=yes]? no
....
root@bs2020:~# dpkg-reconfigure -p medium lxd
... no yes br0...
Warning: Stopping lxd.service, but it can still be activated by:
	lxd.socket

root@bs2020:~# lxc-create -n naomi -t ubuntu -B zfs --zfsroot=lxd4infra
lxc.rootfs = /var/lib/lxc/naomi/rootfs
lxc.rootfs.backend = zfs
lxc.utsname = naomi
lxc.arch = amd64
..
root@bs2020:~# nano /var/lib/lxc/naomi/config
..... check network ....
# Network configuration
lxc.network.type = veth
lxc.network.link = br0
lxc.network.flags = up
lxc.network.hwaddr = 00:16:3e:dc:6d:b4
# Assign static IP Address (currently done by continer)
#lxc.network.ipv4 = 192.168.1.161/24
#lxc.network.ipv4.gateway = 192.168.1.1
..... add this ....
# Autostart
lxc.start.auto = 1
lxc.start.delay = 5
lxc.start.order = 100
....
root@bs2020~# reboot
```	
### adding admin users and basic services (lock ubuntu user before starting network)
	
```
root@bs2020~# lxc-attach -n naomi
root@naomi:~# passwd -l ubuntu 
root@naomi:~# vi /etc/network/interfaces
... add the following ...
auto eth0
iface eth0 inet static
		address 198.202.31.142/25
		gateway 198.202.31.129
		dns-nameservers 198.202.31.132 198.202.31.141 8.8.8.8
		dns-search vpn suspectdevices.com digithink.com

root@naomi:~# ifdown eth0 && ifup eth0
root@naomi:~# ping digithink.com
root@naomi:~# apt-get update
root@naomi:~# apt-get install openssl-server nano
root@naomi:~# useradd -Gsudo,root -m -c"Donald Delmar Davis" feurig
root@naomi:~# useradd -Gsudo,root -m -c"Joe Dumoulin" joe
root@naomi:~# vipw -s
... paste hash from other system....
root@naomi:~# tail -2 /etc/passwd >passwd.add
root@naomi:~# tail -2 /etc/shadow >shadow.add
root@naomi:~# tar -czvf fnj.tgz /home
root@naomi:~# exit 
root@bs2020~# cp /var/lib/lxc/naomi/rootfs/root/*.add ~feurig/
root@bs2020~# cp /var/lib/lxc/naomi/rootfs/root/fnj.tgz ~feurig/
```	
### tuning bs2020
TODO:
https://github.com/lxc/lxd/blob/master/doc/production-setup.md

## devstack lxc container (FAIL)

This does not work. As far as I can tell you can only install devstack on raw hardware and let it install all of its ever moving dependencies. I was able to do this where pike was 6 months ago but not uninstall and reinstall is using the same version. 

I don't believe it can trust anything this moving to be sane let alone secure.

SEE: GoodByeOpenstack

I may attempt this again within a KVM once I establish that the KVM framework is securable and that it will play nice with the existing containers.

## LXD Container and Docker Install

SEE: [wiki:LXDContainerWithDockerNotes  Creating LXD Container with static ip and Docker Profile]

### lxc docker references
* https://www.flockport.com/lxc-vs-docker/
* https://www.upguard.com/articles/docker-vs-lxc
* http://www.zdnet.com/article/ubuntu-lxd-not-a-docker-replacement-a-docker-enhancement/
* https://stackoverflow.com/questions/37227349/unable-to-start-docker-service-in-ubuntu-16-04
* https://stackoverflow.com/questions/32002882/error-starting-docker-daemon-on-ubuntu-14-04-devices-cgroup-isnt-mounted
### control groups / other related references
* https://help.ubuntu.com/lts/serverguide/cgroups-overview.html
* https://askubuntu.com/questions/836469/install-cgconfig-in-ubuntu-16-04
* https://help.ubuntu.com/lts/serverguide/cgroups.html
#### lxc references

* https://www.ubuntu.com/containers/lxd
* https://insights.ubuntu.com/2016/04/07/lxd-networking-lxdbr0-explained/
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/
* https://www.simpleprecision.com/ubuntu-16-04-lxd-networking-simple-bridge/
* https://askubuntu.com/questions/453659/lxc-containers-fail-to-autoboot-in-14-04-trusty-using-lxc-start-auto-1
* https://help.ubuntu.com/lts/serverguide/lxc.html
* http://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/setup-linux-container-with-lxc-on-ubuntu-16-04-14-04.html
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/
* https://stgraber.org/2016/03/15/lxd-2-0-installing-and-configuring-lxd-212/
* https://wiki.ubuntu.com/LxcSecurity
* https://insights.ubuntu.com/2016/03/16/lxd-2-0-installing-and-configuring-lxd-212/

## fuckups
* openstack/devstack shits all over your server you uninstall it by starting over
  * CHECK TO MAKE SURE YOU ARE IN A CONTAINER BEFORE INSTALLING THE POS THE BARE METAL INTALL IS TOLERABLE BUT NOT FUN.
* installing the virtual server host installs KVM and its kernel. uninstalling it leaves you with a kernel that can't find the network.
* don't press f10 during boot whatever you do and if you do follow this...
  http://crtech.tips/lifecycle-controller-hanging-during-post/
* do not give br0 an address as it will then become a public facing interface with direct access to the host server. 
* local.conf password can't contain any shell characters (%$@!) much like the puppet installer...
* host must also have bridge tables (ebtables)  and openvswitch installed.
* kernel modules needed in lxc containers need to be installed in the host. 
* deleting container zfs pool and storage without telling lxd not to use it is problematic.
   Hint
  	
	root@bs2020:~# lxc config show
	config:
	  storage.zfs_pool_name: lxd4dev
	