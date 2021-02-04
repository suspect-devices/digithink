# HP Z400 notes

### What to do when you get a desktop version of ubuntu and you want a server
	
	sudo bash
	apt-get update&&apt-get dist-upgrade && apt-get autoremove
	nano /etc/hostname 
	
	
	root@joey:~# cd /etc/netplan/
	root@joey:~# mv 01-network-manager-all.yaml /tmp/
	root@joey:~# nano 50-cloud-init.yaml
	network:
	  version: 2
	  renderer: networkd
	  ethernets:
	    enp1s0:
	        dhcp4: no
	        dhcp6: no
	  bridges:
	    br0:
	        dhcp4: no
	        dhcp6: no
	        addresses:
	            - 192.168.0.65/24
	        gateway4: 192.168.0.1
	        nameservers:
	            addresses:
	                - 192.168.0.1
	                - 198.202.31.141
	        interfaces:
	            - enp1s0
	
	root@joey:~# netplan apply
	root@joey:~# reboot
	
	
	root@joey:~# apt-get install openssh-server
	
	
	root@joey:~# nano /etc/default/grub
	root@joey:~# update-grub
	root@joey:~# systemctl enable multi-user.target --force
	root@joey:~# systemctl set-default multi-user.target 
	root@joey:~# reboot
	
## Memory
Looking at the memory usage for that standalone desktop it seems like we could get by with 4G until we decide to use zfs or containers. Our file server is running 3 containers and 7T of zfs and uses 12.8G.(out of 21)

The cheapest memory I could find at present is on eBay at $4/G
https://www.ebay.com/itm/NEW-8GB-2x4GB-Memory-RAM-PC3-10600-ECC-Unbuffered-HP-Compaq-Workstation-Z400/221132609031?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649

### On Board "Fake" Raid
The bios raid on the hpz400 is a bastardized spitwad created by intel hp and only seems to play well with micro$oft. The drivers which kind of worked under dmraid have been integrated into linux's mdraid drivers. The newfangled installer on 18.04 server (subiquity) breaks on it. The alternative installer installs an os on the raid array but it won't boot. You can boot it from another disk but it won't boot by itself. 

#### Making it work
Since I purchased a 240G ssd for this server I installed ubuntu manually to a 10G partition on it, When installing the os activate the intel raid but not the sata raid. Rebooting the box gives you the option of booting to the bios raid array. From there you can chroot onto the boot disk and update the grub default to boot the other disk.

	
	root@joey:~# mount /dev/sdd1 /mnt
	root@joey:~# mount -t proc proc /mnt/proc
	root@joey:~# mount -t sysfs sys /mnt/sys
	root@joey:~# mount -o bind /dev /mnt/dev
	root@joey:~# chroot /mnt
	root@joey:/# cd etc
	root@joey:/etc# nano default/grub
	...
	GRUB_DEFAULT=2
	root@joey:/etc# update-grub
	

### On the other hand
https://www.newegg.com/Product/Product.aspx?Item=9SIAC0F8UV0008&ignorebbr=1&source=region&nm_mc=KNC-GoogleMKP-PC&cm_mmc=KNC-GoogleMKP-PC-_-pla-PC+Server+and+Parts-_-Hard+Drive+Controllers+%2F+RAID+Cards-_-9SIAC0F8UV0008&gclid=CjwKCAjwza_mBRBTEiwASDWVvrfrvrffm4o0noMgtv3UEV7bdZpf1JgLXy4v99kFnn_iNhMc7H2bPhoC7YoQAvD_BwE&gclsrc=aw.ds
'' Note: There may be a bios upgrade to fix this however z400 will not boot from SmartArray P810 either.
### Processor
System !#1
	
	root@annie:~# dmesg|grep smp
	[    0.000000] smpboot: Allowing 16 CPUs, 8 hotplug CPUs
	[    0.044000] smpboot: CPU0: Intel(R) Xeon(R) CPU           W3520  @ 2.67GHz (family: 0x6, model: 0x1a, stepping: 0x5)
	[    0.044000] smp: Bringing up secondary CPUs ...
	[    0.062447] smp: Brought up 1 node, 8 CPUs
	[    0.062447] smpboot: Max logical packages: 2
	[    0.064004] smpboot: Total of 8 processors activated (42670.64 BogoMIPS)
	
System !#2
	
	root@joey:~# dmesg|grep smp
	[    0.000000] smpboot: Allowing 16 CPUs, 14 hotplug CPUs
	[    0.044000] smpboot: CPU0: Intel(R) Xeon(R) CPU           W3503  @ 2.40GHz (family: 0x6, model: 0x1a, stepping: 0x5)
	[    0.044000] smp: Bringing up secondary CPUs ...
	[    0.046748] smp: Brought up 1 node, 2 CPUs
	[    0.046748] smpboot: Max logical packages: 8
	[    0.046748] smpboot: Total of 2 processors activated (9599.50 BogoMIPS)
	root@joey:~# 
	
_Same after upgrade to 1xX5650 $10 on eBay._
	
	root@DeeDee:~# dmesg|grep smp
	[    0.000000] smpboot: Allowing 16 CPUs, 10 hotplug CPUs
	[    0.044000] smpboot: CPU0: Intel(R) Xeon(R) CPU           X5650  @ 2.67GHz (family: 0x6, model: 0x2c, stepping: 0x2)
	[    0.044000] smp: Bringing up secondary CPUs ...
	[    0.060027] smp: Brought up 1 node, 6 CPUs
	[    0.060027] smpboot: Max logical packages: 3
	[    0.060027] smpboot: Total of 6 processors activated (32002.70 BogoMIPS)
	
Compared to BS2020:

	
	root@bs2020:~# dmesg|grep smp
	[    0.000000] smpboot: Allowing 24 CPUs, 0 hotplug CPUs
	[    0.164444] smpboot: CPU 0 Converting physical 1 to logical package 0
	[    0.172000] smpboot: CPU0: Intel(R) Xeon(R) CPU           X5650  @ 2.67GHz (family: 0x6, model: 0x2c, stepping: 0x2)
	[    0.216015] smp: Bringing up secondary CPUs ...
	[    0.004000] smpboot: CPU 1 Converting physical 0 to logical package 1
	[    0.474623] smp: Brought up 2 nodes, 24 CPUs
	[    0.480002] smpboot: Max logical packages: 2
	[    0.484002] smpboot: Total of 24 processors activated (127681.26 BogoMIPS)
	

and kb2018

	
	root@kb2018:~# dmesg|grep smp
	[    0.000000] smpboot: Allowing 32 CPUs, 16 hotplug CPUs
	[    0.140000] smpboot: CPU0: Intel(R) Xeon(R) CPU           E5640  @ 2.67GHz (family: 0x6, model: 0x2c, stepping: 0x2)
	[    0.176015] smp: Bringing up secondary CPUs ...
	[    0.342596] smp: Brought up 2 nodes, 16 CPUs
	[    0.346074] smpboot: Max logical packages: 4
	[    0.348004] smpboot: Total of 16 processors activated (85310.05 BogoMIPS)
	

### Upgrading the Processor
According to [this thread](https://h30434.www3.hp.com/t5/Business-PCs-Workstations-and-Point-of-Sale-Systems/HP-Z400-CPU-upgrade/td-p/5048908) the z400 with the 6 memory slots will support the Xeon 56xx family.
https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/xeon-5600-brief.pdf

I purchased one on eBay for 10 bucks. I probably should have purchased 2

https://www.ebay.com/itm/163034026449

