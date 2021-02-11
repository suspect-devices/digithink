<!-- ResliverFailureNotes, Version: 1, Modified: 2018/12/02, Author: trac -->
#Foobarred zfs filesystem

When replacing our new disks there were hard errors on the disk being reslivered from. 
(spot the error....) 
	
	root@bs2020:~# zpool status -v
	  pool: devel
	 state: DEGRADED
	status: One or more devices has experienced an error resulting in data
		corruption.  Applications may be affected.
	action: Restore the file in question if possible.  Otherwise restore the
		entire pool from backup.
	   see: http://zfsonlinux.org/msg/ZFS-8000-8A
	  scan: resilvered 9.95G in 0h6m with 4 errors on Fri Nov 16 14:04:48 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		devel                       DEGRADED    10     0     0
		  mirror-0                  DEGRADED    23     0     4
		    scsi-35000c50047d16807  DEGRADED    40     0    12  too many errors
		    scsi-35000c50047d0926f  ONLINE       0     0    27
	
	errors: Permanent errors have been detected in the following files:
	
	        devel/containers/naomi7oct2018:/rootfs/home/feurig/mailstuff.tgz
	        devel/containers/naomi7oct2018:/rootfs/usr/lib/x86_64-linux-gnu/gconv/UTF-7.so
	        devel/containers/naomi7oct2018:/old.rootfs/home/feurig/var/lib/lxc/naomi/rootfs/home/feurig/mailstuff.tgz
	        devel/containers/naomi7oct2018:/old.rootfs/home/feurig/var/lib/lxc/naomi/rootfs/home/don/Maildir/.INBOX.arduino/cur/1441292156.M90971P8887.bernie,S=8756,W=8933:2,Sab
	
	  pool: infra
	 state: ONLINE
	  scan: scrub repaired 0B in 0h0m with 0 errors on Sun Nov 11 00:24:23 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		infra                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000cca00b33a264  ONLINE       0     0     0
		    scsi-350000395a8336d34  ONLINE       0     0     0
	
	errors: No known data errors
	root@bs2020:~# 
	
	
	
		sync [pool] ...
	root@bs2020:~# zpool detach devel scsi-35000c50047d0926f
	root@bs2020:~# zpool status
	  pool: devel
	 state: DEGRADED
	status: One or more devices has experienced an error resulting in data
		corruption.  Applications may be affected.
	action: Restore the file in question if possible.  Otherwise restore the
		entire pool from backup.
	   see: http://zfsonlinux.org/msg/ZFS-8000-8A
	  scan: resilvered 9.95G in 0h6m with 4 errors on Fri Nov 16 14:04:48 2018
	config:
	
		NAME                      STATE     READ WRITE CKSUM
		devel                     DEGRADED    10     0     0
		  scsi-35000c50047d16807  DEGRADED    40     0    12  too many errors
	
	errors: 4 data errors, use '-v' for a list
	
	  pool: infra
	 state: ONLINE
	  scan: scrub repaired 0B in 0h0m with 0 errors on Sun Nov 11 00:24:23 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		infra                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000cca00b33a264  ONLINE       0     0     0
		    scsi-350000395a8336d34  ONLINE       0     0     0
	
	errors: No known data errors
	
	
	  pool: devel
	 state: DEGRADED
	status: One or more devices is currently being resilvered.  The pool will
		continue to function, possibly in a degraded state.
	action: Wait for the resilver to complete.
	  scan: resilver in progress since Fri Nov 16 14:49:37 2018
		1.32G scanned out of 9.95G at 16.0M/s, 0h9m to go
		1.32G resilvered, 13.31% done
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		devel                       DEGRADED    10     0     0
		  replacing-0               DEGRADED     0     0     0
		    scsi-35000c50047d16807  DEGRADED    40     0    12  too many errors
		    scsi-35000c50047d0926f  ONLINE       0     0     0  (resilvering)
	
	errors: 4 data errors, use '-v' for a list
	
	  pool: infra
	 state: ONLINE
	  scan: scrub repaired 0B in 0h0m with 0 errors on Sun Nov 11 00:24:23 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		infra                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000cca00b33a264  ONLINE       0     0     0
		    scsi-350000395a8336d34  ONLINE       0     0     0
	
	errors: No known data errors
	root@bs2020:~# zpool status[ 9307.615155] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9309.788008] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9312.115335] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9313.886154] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9315.603474] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9421.337403] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9424.263000] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9426.668087] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9428.468338] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9430.192036] print_req_error: critical medium error, dev sdc, sector 45059769
	[ 9502.892589] print_req_error: critical medium error, dev sdc, sector 99975477
	[ 9505.406331] print_req_error: critical medium error, dev sdc, sector 99975477
	[ 9628.405254] print_req_error: critical medium error, dev sdc, sector 106690474
	[ 9630.596015] print_req_error: critical medium error, dev sdc, sector 106690474
	[ 9638.557126] print_req_error: critical medium error, dev sdc, sector 107074277
	[ 9641.058573] print_req_error: critical medium error, dev sdc, sector 107074277
	