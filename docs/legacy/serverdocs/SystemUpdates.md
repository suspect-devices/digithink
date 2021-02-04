When you log into your ubunty cloud server it will greet you with most of what need to know to keep it up and running.
	
	Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-74-generic x86_64)
	
	 * Documentation:  https://help.ubuntu.com/
	
	  System information as of Thu Apr  7 19:51:52 UTC 2016
	
	  System load:  0.0                Processes:           131
	  Usage of /:   70.9% of 29.39GB   Users logged in:     0
	  Memory usage: 29%                IP address for eth0: 172.31.16.108
	  Swap usage:   0%
	
	  Graph this data and manage this system at:
	    https://landscape.canonical.com/
	
	  Get cloud support with Ubuntu Advantage Cloud Guest:
	    http://www.ubuntu.com/business/services/cloud
	
	13 packages can be updated.
	8 updates are security updates.
	
	
*** System restart required ***
	Last login: Mon Apr  4 18:58:15 2016 from 71-222-65-56.ptld.qwest.net
	don@cloud:~$
	
To update the packages use apt-get update to refresh the package lists. You will need to escalate privilages (become root)
	
	don@cloud:~$ sudo bash
	[sudo] password for don: 
	Sorry, try again.
	[sudo] password for don: 
	root@cloud:~# apt-get update
	Ign http://us-west-2.ec2.archive.ubuntu.com trusty InRelease
	Get:1 http://us-west-2.ec2.archive.ubuntu.com trusty-updates InRelease [65.9 kB]
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty Release.gpg                 
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty Release                     
	Get:2 http://us-west-2.ec2.archive.ubuntu.com trusty-updates/main Sources [271 kB]
	Get:3 http://us-west-2.ec2.archive.ubuntu.com trusty-updates/universe Sources [152 kB]
	Get:4 http://us-west-2.ec2.archive.ubuntu.com trusty-updates/main amd64 Packages [753 kB]
	Get:5 http://us-west-2.ec2.archive.ubuntu.com trusty-updates/universe amd64 Packages [358 kB]
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty-updates/main Translation-en 
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty-updates/universe Translation-en
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/main Sources               
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/universe Sources           
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/main amd64 Packages        
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/universe amd64 Packages    
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/main Translation-en        
	Hit http://us-west-2.ec2.archive.ubuntu.com trusty/universe Translation-en    
	Ign http://us-west-2.ec2.archive.ubuntu.com trusty/main Translation-en_US      
	Ign http://us-west-2.ec2.archive.ubuntu.com trusty/universe Translation-en_US  
	Get:6 http://security.ubuntu.com trusty-security InRelease [65.9 kB]           
	Get:7 http://security.ubuntu.com trusty-security/main Sources [110 kB]         
	Get:8 http://security.ubuntu.com trusty-security/universe Sources [35.2 kB]
	Get:9 http://security.ubuntu.com trusty-security/main amd64 Packages [455 kB]
	Get:10 http://security.ubuntu.com trusty-security/universe amd64 Packages [126 kB]
	Hit http://security.ubuntu.com trusty-security/main Translation-en
	Hit http://security.ubuntu.com trusty-security/universe Translation-en
	Fetched 2,393 kB in 3s (679 kB/s)
	Reading package lists... Done
	root@cloud:~#
	
once this is done you can update all of the installed packages to the currently supported versions by using the dist-upgrade command.
	
	root@cloud:~# apt-get dist-upgrade
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	Calculating upgrade... Done
	The following packages were automatically installed and are no longer required:
	  linux-headers-3.13.0-76 linux-headers-3.13.0-76-generic
	  linux-headers-3.13.0-77 linux-headers-3.13.0-77-generic
	  linux-image-3.13.0-76-generic linux-image-3.13.0-77-generic
	Use 'apt-get autoremove' to remove them.
	The following NEW packages will be installed:
	  linux-headers-3.13.0-85 linux-headers-3.13.0-85-generic
	  linux-image-3.13.0-85-generic
	The following packages will be upgraded:
	  apt apt-transport-https apt-utils libapt-inst1.5 libapt-pkg4.12 libpq5
	  linux-headers-generic linux-headers-virtual linux-image-virtual
	  linux-libc-dev linux-virtual postgresql-9.3 postgresql-client-9.3
	  postgresql-contrib-9.3 postgresql-doc-9.3
	15 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
	Need to get 33.2 MB of archives.
	After this operation, 120 MB of additional disk space will be used.
	Do you want to continue? [Y/n] 
	Get:1 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main libapt-pkg4.12 amd64 1.0.1ubuntu2.12 [637 kB]
	Get:2 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main apt amd64 1.0.1ubuntu2.12 [954 kB]
	Get:3 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main libapt-inst1.5 amd64 1.0.1ubuntu2.12 [58.6 kB]
	Get:4 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-image-3.13.0-85-generic amd64 3.13.0-85.129 [15.2 MB]
	Get:5 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main apt-utils amd64 1.0.1ubuntu2.12 [172 kB]
	Get:6 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main apt-transport-https amd64 1.0.1ubuntu2.12 [25.1 kB]
	Get:7 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main libpq5 amd64 9.3.12-0ubuntu0.14.04 [78.5 kB]
	Get:8 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-headers-3.13.0-85 all 3.13.0-85.129 [8,887 kB]
	Get:9 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-headers-3.13.0-85-generic amd64 3.13.0-85.129 [707 kB]
	Get:10 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-virtual amd64 3.13.0.85.91 [1,778 B]
	Get:11 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-image-virtual amd64 3.13.0.85.91 [2,240 B]
	Get:12 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-headers-virtual amd64 3.13.0.85.91 [1,756 B]
	Get:13 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-headers-generic amd64 3.13.0.85.91 [2,230 B]
	Get:14 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main linux-libc-dev amd64 3.13.0-85.129 [775 kB]
	Get:15 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main postgresql-contrib-9.3 amd64 9.3.12-0ubuntu0.14.04 [401 kB]
	Get:16 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main postgresql-client-9.3 amd64 9.3.12-0ubuntu0.14.04 [785 kB]
	Get:17 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main postgresql-9.3 amd64 9.3.12-0ubuntu0.14.04 [2,691 kB]
	Get:18 http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates/main postgresql-doc-9.3 all 9.3.12-0ubuntu0.14.04 [1,780 kB]
	Fetched 33.2 MB in 0s (36.5 MB/s)          
	(Reading database ... 163885 files and directories currently installed.)
	Preparing to unpack .../libapt-pkg4.12_1.0.1ubuntu2.12_amd64.deb ...
	Unpacking libapt-pkg4.12:amd64 (1.0.1ubuntu2.12) over (1.0.1ubuntu2.11) ...
	Setting up libapt-pkg4.12:amd64 (1.0.1ubuntu2.12) ...
	Processing triggers for libc-bin (2.19-0ubuntu6.7) ...
	(Reading database ... 163885 files and directories currently installed.)
	Preparing to unpack .../apt_1.0.1ubuntu2.12_amd64.deb ...
	Unpacking apt (1.0.1ubuntu2.12) over (1.0.1ubuntu2.11) ...
	Processing triggers for man-db (2.6.7.1-1ubuntu1) ...
	Setting up apt (1.0.1ubuntu2.12) ...
	Processing triggers for libc-bin (2.19-0ubuntu6.7) ...
	(Reading database ... 163885 files and directories currently installed.)
	Preparing to unpack .../libapt-inst1.5_1.0.1ubuntu2.12_amd64.deb ...
	Unpacking libapt-inst1.5:amd64 (1.0.1ubuntu2.12) over (1.0.1ubuntu2.11) ...
	Selecting previously unselected package linux-image-3.13.0-85-generic.
	Preparing to unpack .../linux-image-3.13.0-85-generic_3.13.0-85.129_amd64.deb ...
	Done.
	Unpacking linux-image-3.13.0-85-generic (3.13.0-85.129) ...
	Preparing to unpack .../apt-utils_1.0.1ubuntu2.12_amd64.deb ...
	Unpacking apt-utils (1.0.1ubuntu2.12) over (1.0.1ubuntu2.11) ...
	Preparing to unpack .../apt-transport-https_1.0.1ubuntu2.12_amd64.deb ...
	Unpacking apt-transport-https (1.0.1ubuntu2.12) over (1.0.1ubuntu2.11) ...
	Preparing to unpack .../libpq5_9.3.12-0ubuntu0.14.04_amd64.deb ...
	Unpacking libpq5 (9.3.12-0ubuntu0.14.04) over (9.3.11-0ubuntu0.14.04) ...
	Selecting previously unselected package linux-headers-3.13.0-85.
	Preparing to unpack .../linux-headers-3.13.0-85_3.13.0-85.129_all.deb ...
	Unpacking linux-headers-3.13.0-85 (3.13.0-85.129) ...
	Selecting previously unselected package linux-headers-3.13.0-85-generic.
	Preparing to unpack .../linux-headers-3.13.0-85-generic_3.13.0-85.129_amd64.deb ...
	Unpacking linux-headers-3.13.0-85-generic (3.13.0-85.129) ...
	Preparing to unpack .../linux-virtual_3.13.0.85.91_amd64.deb ...
	Unpacking linux-virtual (3.13.0.85.91) over (3.13.0.83.89) ...
	Preparing to unpack .../linux-image-virtual_3.13.0.85.91_amd64.deb ...
	Unpacking linux-image-virtual (3.13.0.85.91) over (3.13.0.83.89) ...
	Preparing to unpack .../linux-headers-virtual_3.13.0.85.91_amd64.deb ...
	Unpacking linux-headers-virtual (3.13.0.85.91) over (3.13.0.83.89) ...
	Preparing to unpack .../linux-headers-generic_3.13.0.85.91_amd64.deb ...
	Unpacking linux-headers-generic (3.13.0.85.91) over (3.13.0.83.89) ...
	Preparing to unpack .../linux-libc-dev_3.13.0-85.129_amd64.deb ...
	Unpacking linux-libc-dev:amd64 (3.13.0-85.129) over (3.13.0-83.127) ...
	Preparing to unpack .../postgresql-contrib-9.3_9.3.12-0ubuntu0.14.04_amd64.deb ...
	Unpacking postgresql-contrib-9.3 (9.3.12-0ubuntu0.14.04) over (9.3.11-0ubuntu0.14.04) ...
	Preparing to unpack .../postgresql-client-9.3_9.3.12-0ubuntu0.14.04_amd64.deb ...
	Unpacking postgresql-client-9.3 (9.3.12-0ubuntu0.14.04) over (9.3.11-0ubuntu0.14.04) ...
	Preparing to unpack .../postgresql-9.3_9.3.12-0ubuntu0.14.04_amd64.deb ...
	 * Stopping PostgreSQL 9.3 database server                                                                            [ OK ] 
	Unpacking postgresql-9.3 (9.3.12-0ubuntu0.14.04) over (9.3.11-0ubuntu0.14.04) ...
	Preparing to unpack .../postgresql-doc-9.3_9.3.12-0ubuntu0.14.04_all.deb ...
	Unpacking postgresql-doc-9.3 (9.3.12-0ubuntu0.14.04) over (9.3.11-0ubuntu0.14.04) ...
	Processing triggers for man-db (2.6.7.1-1ubuntu1) ...
	Processing triggers for postgresql-common (154ubuntu1) ...
	Building PostgreSQL dictionaries from installed myspell/hunspell packages...
	Removing obsolete dictionary files:
	Setting up libapt-inst1.5:amd64 (1.0.1ubuntu2.12) ...
	Setting up linux-image-3.13.0-85-generic (3.13.0-85.129) ...
	Running depmod.
	update-initramfs: deferring update (hook will be called later)
	Examining /etc/kernel/postinst.d.
	run-parts: executing /etc/kernel/postinst.d/apt-auto-removal 3.13.0-85-generic /boot/vmlinuz-3.13.0-85-generic
	run-parts: executing /etc/kernel/postinst.d/initramfs-tools 3.13.0-85-generic /boot/vmlinuz-3.13.0-85-generic
	update-initramfs: Generating /boot/initrd.img-3.13.0-85-generic
	run-parts: executing /etc/kernel/postinst.d/update-notifier 3.13.0-85-generic /boot/vmlinuz-3.13.0-85-generic
	run-parts: executing /etc/kernel/postinst.d/x-grub-legacy-ec2 3.13.0-85-generic /boot/vmlinuz-3.13.0-85-generic
	Searching for GRUB installation directory ... found: /boot/grub
	Searching for default file ... found: /boot/grub/default
	Testing for an existing GRUB menu.lst file ... found: /boot/grub/menu.lst
	Searching for splash image ... none found, skipping ...
	Found kernel: /boot/vmlinuz-3.13.0-85-generic
	Found kernel: /boot/vmlinuz-3.13.0-83-generic
	Found kernel: /boot/vmlinuz-3.13.0-79-generic
	Found kernel: /boot/vmlinuz-3.13.0-77-generic
	Found kernel: /boot/vmlinuz-3.13.0-76-generic
	Found kernel: /boot/vmlinuz-3.13.0-74-generic
	Replacing config file /run/grub/menu.lst with new version
	Updating /boot/grub/menu.lst ... done
	
	run-parts: executing /etc/kernel/postinst.d/zz-update-grub 3.13.0-85-generic /boot/vmlinuz-3.13.0-85-generic
	Generating grub configuration file ...
	Found linux image: /boot/vmlinuz-3.13.0-85-generic
	Found initrd image: /boot/initrd.img-3.13.0-85-generic
	Found linux image: /boot/vmlinuz-3.13.0-83-generic
	Found initrd image: /boot/initrd.img-3.13.0-83-generic
	Found linux image: /boot/vmlinuz-3.13.0-79-generic
	Found initrd image: /boot/initrd.img-3.13.0-79-generic
	Found linux image: /boot/vmlinuz-3.13.0-77-generic
	Found initrd image: /boot/initrd.img-3.13.0-77-generic
	Found linux image: /boot/vmlinuz-3.13.0-76-generic
	Found initrd image: /boot/initrd.img-3.13.0-76-generic
	Found linux image: /boot/vmlinuz-3.13.0-74-generic
	Found initrd image: /boot/initrd.img-3.13.0-74-generic
	done
	Setting up apt-utils (1.0.1ubuntu2.12) ...
	Setting up apt-transport-https (1.0.1ubuntu2.12) ...
	Setting up libpq5 (9.3.12-0ubuntu0.14.04) ...
	Setting up linux-headers-3.13.0-85 (3.13.0-85.129) ...
	Setting up linux-headers-3.13.0-85-generic (3.13.0-85.129) ...
	Setting up linux-image-virtual (3.13.0.85.91) ...
	Setting up linux-headers-generic (3.13.0.85.91) ...
	Setting up linux-headers-virtual (3.13.0.85.91) ...
	Setting up linux-virtual (3.13.0.85.91) ...
	Setting up linux-libc-dev:amd64 (3.13.0-85.129) ...
	Setting up postgresql-client-9.3 (9.3.12-0ubuntu0.14.04) ...
	Setting up postgresql-9.3 (9.3.12-0ubuntu0.14.04) ...
	 * Starting PostgreSQL 9.3 database server                                                                            [ OK ] 
	Setting up postgresql-contrib-9.3 (9.3.12-0ubuntu0.14.04) ...
	Setting up postgresql-doc-9.3 (9.3.12-0ubuntu0.14.04) ...
	Processing triggers for libc-bin (2.19-0ubuntu6.7) ...
	

If one of the updates includes a kernel or if system restart required a system reboot should be scheduled.

