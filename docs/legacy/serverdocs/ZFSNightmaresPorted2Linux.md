# ZFS IS ALL THE RAGE!
Zfs is recomended  by the UBUNTU team for LXC/LXD and it has its positives but just like everything else the damned kids fixed is pleanty fucking broke. It does not play well with others and it will fuck you in the most subtle and substantial ways.
* look at the disks.

	
	root@bs2020:~# fdisk -l
	Disk /dev/sda: 136.8 GiB, 146815733760 bytes, 286749480 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0x264ef27d
	
	Device     Boot Start       End   Sectors   Size Id Type
	/dev/sda1        2048 286749479 286747432 136.7G 83 Linux
	
	
	Disk /dev/sdb: 136.8 GiB, 146815733760 bytes, 286749480 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0xc06248cd
	
	Device     Boot    Start       End   Sectors  Size Id Type
	/dev/sdb1           2048  85448703  85446656 40.8G 83 Linux
	/dev/sdb2       85450750 286748671 201297922   96G  5 Extended
	/dev/sdb5       85450752 286748671 201297920   96G 82 Linux swap / Solaris
	
	
	Disk /dev/sdc: 136.8 GiB, 146815733760 bytes, 286749480 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: gpt
	Disk identifier: 037F919F-B203-449D-A74D-9F285A3B89BD
	
	Device     Start       End   Sectors   Size Type
	/dev/sdc1   2048 286749446 286747399 136.7G Linux filesystem
	
	
	Disk /dev/sde: 136.8 GiB, 146815733760 bytes, 286749480 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: gpt
	Disk identifier: 66247EC5-E595-44A0-B6B8-F4A18179D457
	
	Device     Start       End   Sectors   Size Type
	/dev/sde1   2048 286749446 286747399 136.7G Linux filesystem
	
	
	Disk /dev/sdd: 465.8 GiB, 500107862016 bytes, 976773168 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: gpt
	Disk identifier: C1068A13-6375-48DE-A72B-0F9B3223B6DE
	
	Device     Start       End   Sectors   Size Type
	/dev/sdd1   2048 976773134 976771087 465.8G Linux filesystem
	
	
	root@bs2020:~# 
	
* there is no connection between this and zfs.
	
	root@bs2020:~# zpool status
	  pool: lxd4dev
	 state: ONLINE
	  scan: scrub repaired 0 in 0h4m with 0 errors on Sun Jan 14 00:28:08 2018
	config:
	
		NAME        STATE     READ WRITE CKSUM
		lxd4dev     ONLINE       0     0     0
		  sdc1      ONLINE       0     0     0
	
	errors: No known data errors
	
	  pool: lxd4infra
	 state: ONLINE
	  scan: scrub repaired 0 in 0h0m with 0 errors on Sun Jan 14 00:24:49 2018
	config:
	
		NAME        STATE     READ WRITE CKSUM
		lxd4infra   ONLINE       0     0     0
		  sda1      ONLINE       0     0     0
	
	errors: No known data errors
	root@bs2020:~# 
	

if either of these are missing you need to zpool import the disk in its new location. In the long term the disks should be set up to reference their UUIDs but this requires that the pools not be in use (IE Single user mode). This is further complicated by the fact that the pools had to be created in completely different way for lxc and lxd. Hope they fix this in 18.04

## Linkdump
### Good ones
* http://kbdone.com/zfs-snapshots-clones/
* http://manpages.ubuntu.com/manpages/xenial/man8/zfs.8.html
* https://www.howtoforge.com/tutorial/how-to-use-snapshots-clones-and-replication-in-zfs-on-linux/
* 
### Fodder
* https://www.thegeekdiary.com/zfs-tutorials-creating-zfs-snapshot-and-clones/
* http://lxd.readthedocs.io/en/latest/backup/#container-backup-and-restore
* https://forums.freenas.org/index.php?threads/zfs-send-to-external-backup-drive.17850/
* https://www.freebsd.org/cgi/man.cgi?query=zfs
* https://www.datto.com/uk/blog/four-ways-to-use-zfs-snapshots
* https://forum.proxmox.com/threads/adding-ssd-for-cache-zil-l2arc.25187/
* https://www.freebsd.org/cgi/man.cgi?query=zfs