## Netplan / Networkd
Given the success of systemd the kids decided that they needed to rewrite the networking core using a yaml file under /etc/netplan/ and various "renderers". If it all gets too much you can replace it with the legacy system ifupdown and continue to edit /etc/network/interfaces, etc.
	
	apt-get install ifupdown
	
Otherwise read the notes to follow. 

See: [Netplan Documentation (https://netplan.io/)](https://netplan.io/)
### Static Networking with Netplan
Assuming that your cloud configuration does not overwrite it the following file produces a static ip.
	
	oot@phillip:~# cat /etc/netplan/50-cloud-init.yaml 
	network:
	  version: 2
	  ethernets:
	    eth0:
	      dhcp4: no
	      addresses: [198.202.31.223/25]
	      gateway4: 198.202.31.129
	      nameservers:
	        search: [suspectdevices.com fromhell.com vpn]
	        addresses: [198.202.31.141]
	
### Bridge Networking with Netplan
	
	root@annie:~# nano /etc/netplan/01-netcfg.yaml 
	network:
	  version: 2
	  renderer: networkd
	  ethernets:
	    ens6:
	        dhcp4: true
	        dhcp6: no
	    enp1s0:
	        dhcp4: no
	        dhcp6: no
	  bridges:
	    br0:
	        dhcp4: no
	        dhcp6: no
	        addresses:
	            - 192.168.0.66/24
	        gateway4: 192.168.0.1
	        nameservers:
	            addresses:
	                - 192.168.0.1
	                - 198.202.31.141
	        interfaces:
	            - enp1s0
	root@annie:~# netplan apply
	root@annie:~# ip a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
	    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
	    inet 127.0.0.1/8 scope host lo
	       valid_lft forever preferred_lft forever
	  ...
	2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br0 state UP group default qlen 1000
	    link/ether 78:e7:d1:c3:ef:9e brd ff:ff:ff:ff:ff:ff
	3: ens6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
	    link/ether 00:14:d1:25:2b:bc brd ff:ff:ff:ff:ff:ff
	    inet 192.168.2.66/24 brd 192.168.2.255 scope global dynamic ens6
	       valid_lft 43163sec preferred_lft 43163sec
	    inet6 fd5b:a1ad:aeeb::fd0/128 scope global noprefixroute 
	...
	6: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
	    link/ether aa:18:c9:5a:76:d6 brd ff:ff:ff:ff:ff:ff
	    inet 192.168.0.66/24 brd 192.168.0.255 scope global br0
	       valid_lft forever preferred_lft forever
	    inet6 fe80::a818:c9ff:fe5a:76d6/64 scope link 
	       valid_lft forever preferred_lft forever
	root@annie:~# brctl show
	bridge name	bridge id		STP enabled	interfaces
	br0		8000.aa18c95a76d6	no		enp1s0
	root@annie:~# 
	
## And it works for anonymous bridges .... EXCEPT FOR THE BUG
Basically if no address is given for a bridge netplan fails to tell systemd to up the interface anyway and the bridges do not come up. 
	
	root@bs2020:~# nano /etc/netplan/50-cloud-init.yaml 
	# This file is generated from information provided by
	# the datasource.  Changes to it will not persist across an instance.
	# To disable cloud-init's network configuration capabilities, write a file
	# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
	# network: {config: disabled}
	network:
	    version: 2
	    renderer: networkd
	    ethernets:
	        eno1:
	           dhcp4: no
	           addresses: [192.168.31.158/24]
	           gateway4: 192.168.31.1
	           nameservers:
	               search: [suspectdevices.com fromhell.com vpn]
	               addresses: [198.202.31.141]
	        eno2:
	            dhcp4: no
	            optional: true
	        eno3:
	            dhcp4: no
	        eno4:
	            dhcp4: no
	    bridges:
	       br0:
	          dhcp4: no
	          dhcp6: no
	          interfaces:
	              - eno4
	       br1:
	          dhcp4: no
	          dhcp6: no
	          interfaces:
	              - eno3
	
	root@bs2020:~# nano /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg 
	network: {config: disabled}
	root@bs2020:~# netplan apply
	
So you have to create the scripts until they fix this.
	
	root@bs2020:~# nano /etc/systemd/network/br0.network
	[Match]
	Name=br0
	
	[Network]
	LinkLocalAddressing=no
	IPv6AcceptRA=no
	
	root@bs2020:~# nano /etc/systemd/network/br1.network
	[Match]
	Name=br1
	
	[Network]
	LinkLocalAddressing=no
	IPv6AcceptRA=no
	
	
https://bugs.launchpad.net/ubuntu/+source/nplan/+bug/1736975
http://djanotes.blogspot.com/2018/04/anonymous-bridges-in-netplan.html

### Freaking Cloud init
Need to figure out how much damage is done here...

#### Starting with the hostname.
The hostname is now handled by a new command and /etc/cloud/cloud.config needs to be modified to preserve the hostname across boots.
	
	feurig@bs2020:~$ sudo bash
	[sudo] password for feurig: 
	root@bs2020:~# hostnamectl set-hostname bs2020
	root@bs2020:~# nano /etc/cloud/cloud.cfg
	....
	# This will cause the set+update hostname module to not operate (if true)
	preserve_hostname: true
	...
	root@bs2020:~# reboot
	
	
#### Install the root users .
   One would like for the installer to give you some options for installing the admin team but we just paste the hash from one of the other machines into the shadow password file and copy the home directories for their ssh keys. see wiki:kb2018InstallBashHistory
   	
	 ( .. tired of winning .... write up later... )
	
#### Install zfs 
	
	root@bs2020:~# apt-get install nfs-kernel-server samba-common-bin zfsutils-linux
	
* create zfs pools using lxd init.
* make servers available to each other.
* configure outgoing mail.
* install apticron

## Apache2
Big leap in apache version. Lots of configuration changes.

### Link Dump
* https://netplan.io/examples
* https://websiteforstudents.com/configure-static-ip-addresses-on-ubuntu-18-04-beta/
* https://askubuntu.com/questions/1054350/netplan-bridge-for-kvm-on-ubuntu-server-18-04-with-static-ips
https://stackoverflow.com/questions/33377916/migrating-lxc-to-lxd