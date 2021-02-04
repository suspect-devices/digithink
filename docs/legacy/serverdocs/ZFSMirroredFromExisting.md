# ZFS Mirrored data on existing file server## Adding zfs mirror to existing data
On Annie, the Home File Server we have a pair of matched 2T sata disks, one of which contains the majority of the shared data. We want to convert these to a mirrored disk using  ZFS  (thereby securing the existing data). Rather than using entire disks the disks should be partitioned so that they are bootable and can contain a fresh os installation.

_note: the following assumes we have installed some prerequisites...._
	
	root@annie:~# apt-get install  zfsutils-linux parted nfs-kernel-server zfs-initramfs 
	
* First we wipe and partition the unused disk.
	
	root@annie:~# df -k
	Filesystem      1K-blocks      Used  Available Use% Mounted on
	...
	/dev/sdc1      1922728820 905645512  919391248  50% /export
	/dev/sdd1      1921802520     77852 1824032608   1% /archive
	...
	root@annie:~# umount /archive
	... adjust /etc/fstab if necessary ...
	root@annie:~# parted /dev/sdd1
	(parted) mklabel gpt                                                    
	Warning: Partition(s) on /dev/sdd are being used.
	Ignore/Cancel? I                                                          
	(parted) mkpart zfs zfs 0% -100512MB
	(parted) mkpart efi fat32  -100512MB -100000MB
	(parted) mkpart lnx ext2 -100000MB 100%                                   
	(parted) set 2 boot on            
	root@annie:~# reboot                                 
	
* create a zfs pool on the first partition
	
	root@annie:~# zpool create basement -f /dev/disk/by-id/wwn-0x5000039ff3c899c1-part1
	root@annie:~# zpool list
	NAME       SIZE  ALLOC   FREE  EXPANDSZ   FRAG    CAP  DEDUP  HEALTH  ALTROOT
	basement  1.72T   865G   895G         -     0%    49%  1.00x  ONLINE  -
	root@annie:~# df -k
	...
	/dev/sdc1      1922728820 905645512  919391248  50% /export
	...
	basement       1787821824       128 1787821696   1% /basement
	root@annie:~# mkdir /basement/filebox
	root@annie:~# screen mv -v /export/* /basement/filebox/
	...
	root@annie:~# df -k
	...
	/dev/sdc1      1922728820       512 1922728820    0% /export
	...
	basement       1787817216 906994176  880823040  51% /basement
	...
	
* Repartition old drive and add the first partition to  the zfs pool as a mirror.
	
	root@annie:~# umount /export
	... adjust /etc/fstab if necessary ...
	root@annie:~# parted /dev/sdc1
	(parted) mklabel gpt                                                    
	Warning: Partition(s) on /dev/sdc are being used.                                  
	Ignore/Cancel? I                                                          
	
	(parted) mkpart zfs zfs 0% -100512MB
	(parted) mkpart efi fat32  -100512MB -100000MB
	(parted) mkpart lnx ext2 -100000MB 100%                                   
	(parted) set 2 boot on            
	root@annie:~# reboot                                 
	
	root@annie:~# zpool attach -f basement wwn-0x5000039ff3c899c1-part1 wwn-0x5000039ff3c2ca97-part1
	root@annie:~# zpool status 
	... should show both disks and note (reslivering)
	
* wait for reslivering to finish (1.7T took about 1.75 hours)
	
	don@annie:~$ zpool status
	  pool: basement
	 state: ONLINE
	  scan: scrub repaired 0B in 1h44m with 0 errors on Sun Sep  9 02:08:43 2018
	config:
	
		NAME                              STATE     READ WRITE CKSUM
		basement                          ONLINE       0     0     0
		  mirror-0                        ONLINE       0     0     0
		    wwn-0x5000039ff3c899c1-part1  ONLINE       0     0     0
		    wwn-0x5000039ff3c2ca97-part1  ONLINE       0     0     0
	
	errors: No known data errors
	
