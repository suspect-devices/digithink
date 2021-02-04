### Looking at LTS debian/ubuntu 18.04 for the next 5 years (bs2020/phillip)
As an excersize we ran up a 17.10 ubuntu container to see what all was going to break when we upgraded. So far the usual suspects (Network configuration, startup etc) are all fucked up. We upgraded this to 18.04 using do-release-upgrade.
	
	root@phillip:~# do-release-upgrade -d
	
Then we started working on the bullshit.
### Stupid Idea #1 netplan
According to the Release Notes for Bionic Beaver: on top of adding color emojis they rewrote the network management layer based on the worst innovations of modern linux (systemd and NetworManager)

 "Netplan is a YAML network configuration abstraction for various backends (NetworkManager, networkd).

 It is a utility for easily configuring networking on a system. It can be used by writing a YAML description of the required network interfaces with what they should be configured to do. From this description it will generate the required configuration for a chosen renderer tool.

 Netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators, installers, cloud image instantiations, or other OS deployments. During early boot it then generates backend specific configuration files in /run to hand off control of devices to a particular networking daemon."

In otherwords we are ripping up everything and hoping the the details will work themselves out even though they are not defined and buried in several layers of bullshit written by children and adult children (zb your average modern CTO).

## Making it work
After a lot of digging I edited this file on phillip and rebooted the container.
	
	root@phillip:~# nano /etc/netplan/50-cloud-init.yaml 
	# This file is generated from information provided by
	# the datasource.  Changes to it will not persist across an instance.
	# To disable cloud-init's network configuration capabilities, write a file
	# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
	# network: {config: disabled}
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
	
Note that even this file says its generated rather than referenced. Really? 'provided by "the datasource"' WHAT DATASOURCE???? FUCKING KIDS. 
The datasource in this case would be cloud init. In this case cloud init has been told not to configure the network. 
 
 

## linkdump
* https://wiki.ubuntu.com/Netplan/Design
* https://wiki.edubuntu.org/BionicBeaver/ReleaseNotes
* http://www.ubuntugeek.com/how-to-assign-static-ip-address-in-ubuntu-17-10-artful-aardvark.html
* 



