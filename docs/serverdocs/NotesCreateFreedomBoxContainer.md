<!-- NotesCreateFreedomBoxContainer, Version: 6, Modified: 2019/10/05, Author: feurig -->
# Buster Notes

FreedomBox is packaged on Debian 10
### Creating a cloud-init capable Debian/10 container
Download container from images.
	
	root@annie:~# lxc image copy images:debian/10 local: --copy-aliases
	root@annie:~# lxc image list
	+--------------------+--------------+--------+---------------------------------------------+--------+----------+------------------------------+
	|       ALIAS        | FINGERPRINT  | PUBLIC |                 DESCRIPTION                 |  ARCH  |   SIZE   |         UPLOAD DATE          |
	+--------------------+--------------+--------+---------------------------------------------+--------+----------+------------------------------+
	| b (10 more)        | c395a7105278 | no     | ubuntu 18.04 LTS amd64 (release) (20180911) | x86_64 | 173.98MB | Sep 30, 2018 at 4:00am (UTC) |
	+--------------------+--------------+--------+---------------------------------------------+--------+----------+------------------------------+
	| debian/10 (7 more) | ec89a28d9d81 | no     | Debian buster amd64 (20190930_05:24)        | x86_64 | 73.00MB  | Sep 30, 2019 at 3:58pm (UTC) |
	+--------------------+--------------+--------+---------------------------------------------+--------+----------+------------------------------+
	root@annie:~# lxc init debian/10 buster
	Creating buster
	root@annie:~# lxc start buster
	
Copy templates and metadata to image
	
	root@annie:/var/lib/lxd/storage-pools/devil/containers/buster# cat ../viva/metadata.yaml >>metadata.yaml 
	root@annie:/var/lib/lxd/storage-pools/devil/containers/buster# cp -rpv ../viva/templates/
	cloud-init-meta.tpl     cloud-init-network.tpl  cloud-init-user.tpl     cloud-init-vendor.tpl   hostname.tpl            
	root@annie:/var/lib/lxd/storage-pools/devil/containers/buster# cp -rpv ../viva/templates .
	'../viva/templates/cloud-init-meta.tpl' -> './templates/cloud-init-meta.tpl'
	'../viva/templates/cloud-init-network.tpl' -> './templates/cloud-init-network.tpl'
	'../viva/templates/cloud-init-user.tpl' -> './templates/cloud-init-user.tpl'
	'../viva/templates/hostname.tpl' -> './templates/hostname.tpl'
	'../viva/templates/cloud-init-vendor.tpl' -> './templates/cloud-init-vendor.tpl'
	root@annie:/var/lib/lxd/storage-pools/devil/containers/buster# nano metadata.yaml 
	.... delete original templates section and properties from other system ....
	
Add cloud-init, cloud-utils, and ssh server
	
	root@annie:~# lxc exec buster bash
	root@buster:~# apt-get install inetutils-ping nano cloud-init cloud-utils openssh-server python3
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	...
	root@buster:~# nano /etc/network/interfaces.d/50-cloud-init.cfg 
	root@buster:~# rm /etc/network/interfaces
	root@buster:~# ln -s /etc/network/interfaces.d/50-cloud-init.cfg /etc/network/interfaces
	
	root@buster:~# shutdown -h now
	
Publish the image
	
	root@annie:~# lxc publish buster --alias debian/10cloud description="Debian buster plus cloud-init"
	
## Using the container
If you are not going to keep the image you can create it using lxc init.
	
	root@annie:/etc/ansible# lxc init debian/10cloud camo -p susdev19 -p default
	root@annie:/etc/ansible# lxc start camo
	
Or you can add it to /etc/ansible/hosts and use the create-lxc-containers.yml playbook.

	
	root@annie:/etc/ansible# grep camo hosts
	camo  ip_address=192.168.0.253 purpose="Freedombox Test Server"  image_alias=debian/10cloud
	root@annie:/etc/ansible# ansible-playbook playbooks/create-lxd-containers.yml 
	...
	root@annie:/etc/ansible# lxc list
	+------------+---------+----------------------+------+------------+-----------+
	|    NAME    |  STATE  |         IPV4         | IPV6 |    TYPE    | SNAPSHOTS |
	+------------+---------+----------------------+------+------------+-----------+
	| buster     | STOPPED |                      |      | PERSISTENT | 0         |
	+------------+---------+----------------------+------+------------+-----------+
	| camo       | RUNNING | 192.168.0.253 (eth0) |      | PERSISTENT | 0         |
	+------------+---------+----------------------+------+------------+-----------+
	

## Installing freedombox
	 
	# apt-get install freedombox
	
	 
There are a few questions on the install that need to be answered and then its more or less done. 
I am not sure I want it exposed until I figure out how to configure it securely. Am going to run it up on the home server first.
