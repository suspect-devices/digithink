# DL380 Raid Notes
## Problem: Where are my disks???
When we installed the os on our new (to us) prolient DL380, Only a single disk was visible in spite of there having been 6 disks installed. This is because the DL380s disk controller was set up in raid mode an did not expose disks until they were configured as "logical" disks. 

This is unlike the Dell PowerEdge we have which detects and presents the drives in a hot swappable fashion while still allowing some disks to participate in raid arrays.  

Since we use hardware raid mirroring on the boot disks, Adding, removing or replacing disks  requires configuring the raid controller. 
## Using HP utilities to configure the controller without downing the server

HP provides utilities and officially supports bionic and hosts a repo for it. It includes a server that can be accessed graphically as well as a command line interface. [#fn1 (1)]
For the purpose of maintaining disks we only need ssacli and perhaps ssaducli. 

Install the hp supported utilities.
	
	root@kb2018:~# echo "deb http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current non-free" >> /etc/apt/sources.list.d/hp.list
	root@kb2018:~# root@kb2018:/etc/apt# wget http://downloads.linux.hpe.com/SDR/repo/mcp/GPG-KEY-mcp
	--2018-11-12 09:00:29--  http://downloads.linux.hpe.com/SDR/repo/mcp/GPG-KEY-mcp
	Resolving downloads.linux.hpe.com (downloads.linux.hpe.com)... 15.249.152.85
	Connecting to downloads.linux.hpe.com (downloads.linux.hpe.com)|15.249.152.85|:80... connected.
	HTTP request sent, awaiting response... 200 OK
	Length: 994
	Saving to: ‘GPG-KEY-mcp’
	
	GPG-KEY-mcp                                  100%[=============================================================================================>]     994  --.-KB/s    in 0s      
	
	2018-11-12 09:00:30 (90.5 MB/s) - ‘GPG-KEY-mcp’ saved [994/994]
	
	root@kb2018:/etc/apt# apt-key add GPG-KEY-mcp
	OK
	root@kb2018:/etc/apt# apt-get update
	Ign:1 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current InRelease
	Get:2 http://security.ubuntu.com/ubuntu bionic-security InRelease [83.2 kB]                      
	Hit:3 http://us.archive.ubuntu.com/ubuntu bionic InRelease                                           
	Get:4 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release [6,051 B]        
	Get:5 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release.gpg [490 B]                                
	Get:6 http://us.archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]                                                               
	Hit:7 http://archive.ubuntu.com/ubuntu bionic InRelease                                                              
	Ign:5 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release.gpg                                 
	Get:8 http://archive.ubuntu.com/ubuntu bionic-security InRelease [83.2 kB]             
	Get:9 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]                      
	Reading package lists... Done      
	W: GPG error: http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C208ADDE26C2B797
	E: The repository 'http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release' is not signed.
	N: Updating from such a repository can't be done securely, and is therefore disabled by default.
	N: See apt-secure(8) manpage for repository creation and user configuration details.
	root@kb2018:/etc/apt# key=C208ADDE26C2B797
	root@kb2018:/etc/apt# gpg --keyserver keyserver.ubuntu.com --recv-keys $key
	gpg: key C208ADDE26C2B797: public key "Hewlett Packard Enterprise Company RSA-2048-25 <signhp@hpe.com>" imported
	gpg: Total number processed: 1
	gpg:               imported: 1
	root@kb2018:/etc/apt# gpg --armor --export $key |apt-key add -
	OK
	root@kb2018:/etc/apt# apt-get update
	Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [83.2 kB]
	Hit:2 http://us.archive.ubuntu.com/ubuntu bionic InRelease                                                             
	Get:3 http://us.archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]                                                                      
	Hit:4 http://archive.ubuntu.com/ubuntu bionic InRelease                                                                                                      
	Ign:5 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current InRelease                                                                                        
	Get:6 http://archive.ubuntu.com/ubuntu bionic-security InRelease [83.2 kB]                                
	Get:7 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release [6,051 B]                       
	Get:8 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current Release.gpg [490 B]
	Get:9 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]                       
	Get:10 http://downloads.linux.hpe.com/SDR/downloads/MCP/ubuntu bionic/current/non-free amd64 Packages [1,971 B]
	Fetched 352 kB in 1s (288 kB/s)                                        
	Reading package lists... Done
	root@kb2018:/etc/apt# apt-get install ssacli ssaducli
	...
	
Once the issues with his signature were resolved (above) I was able to instal the ssacli. [#fn2 (2)]
#### Seeing the drives
Use the ssacli to show the unassigned drives after inserting fresh disks.
	
	root@kb2018:/etc/apt# ssacli 
	Smart Storage Administrator CLI 3.30.13.0
	Detecting Controllers...Done.
	Type "help" for a list of supported commands.
	Type "exit" to close the console.
	
	=> set target controller slot=0
	
	   "controller slot=0"
	
	=> pd all show
	
	Smart Array P410i in Slot 0 (Embedded)
	
	   Array A
	
	      physicaldrive 2C:1:1 (port 2C:box 1:bay 1, SAS HDD, 146 GB, OK)
	      physicaldrive 2C:1:2 (port 2C:box 1:bay 2, SAS HDD, 146 GB, OK)
	
	   Array B
	
	      physicaldrive 2C:1:3 (port 2C:box 1:bay 3, SATA SSD, 240 GB, OK)
	
	   Array C
	
	      physicaldrive 2C:1:4 (port 2C:box 1:bay 4, SATA SSD, 240 GB, OK)
	
	   Array D
	
	      physicaldrive 3C:1:5 (port 3C:box 1:bay 5, SAS HDD, 300 GB, OK)
	
	   Array E
	
	      physicaldrive 3C:1:6 (port 3C:box 1:bay 6, SAS HDD, 300 GB, OK)
	
	   Unassigned
	
	      physicaldrive 3C:1:7 (port 3C:box 1:bay 7, SAS HDD, 146 GB, OK)
	      physicaldrive 3C:1:8 (port 3C:box 1:bay 8, SAS HDD, 146 GB, OK)
	
	
	

#### letting the OS see the drives
Once we know what drives are available we can create logical drives which will be presented to the os _(assuming the same set target command above)_
	
	=> set target controller slot=0
	...
	=> create type=ld drives=3C:1:7 size=max raid=0  
	=> create type=ld drives=3C:1:8 size=max raid=0
	quit
	
#### Removing drive
Before removing drives you should make sure that they are unmounted or detached (zfs).
After removing a drive you should delete the logical disk that it is associated with. 
	
	
	=> set target controller slot=0
	...
	=> Array G delete
	
 
#### Increasing write performance
once we get a ups we should be able to use the controllers write cache safely.
	
	=> controller slot=0 modify drivewritecache=enable
	
	Warning: Without the proper safety precautions, use of write cache on physical 
	         drives could cause data loss in the event of power failure.  To ensure
	         data is properly protected, use redundant power supplies and
	         Uninterruptible Power Supplies. Also, if you have multiple storage
	         enclosures, all data should be mirrored across them. Use of this
	         feature is not recommended unless these precautions are followed.
	         Continue? (y/n) n
	
	=> 
	
	

See also: [wiki:DL380RaidBios my notes on configuring the disks the hard way]
### footnotes
[=#fn1 1]) This was discovered after digging around for the perccli raid utilities provided by dell (officially supported only on commercial RPM based systems but installable using alien) 

[=#fn2 2]) The biggest pain in the ass other than the weirdness with the public signature was that HP fucking rebranded the hpssacli to ssacli. Most of the good web info and hp docs still reference the old utility name (nothing else changed).

### references
* http://h10032.www1.hp.com/ctg/Manual/c02289065.pdf (2010)
* https://amk1.wordpress.com/2013/11/22/zfs-with-hp-smart-array-p410i/ 
* https://content.etilize.com/User-Manual/1033728289.pdf
* http://www.sysadminshare.com/2012/05/hpacucli-commands-referrence.html
* https://wiki.debian.org/LinuxRaidForAdmins
* https://www.golinuxhub.com/2017/05/hot-swapping-broken-hdd-with-software.html
* https://kallesplayground.wordpress.com/useful-stuff/hp-smart-array-cli-commands-under-esxi/
* http://downloads.linux.hpe.com/SDR/project/mcp/
* https://wiki.debian.org/HP/ProLiant#HP_Repository
* https://binaryimpulse.com/2013/09/hp-array-configuration-utility-command-cheat-sheet/
* https://bibszone.wordpress.com/2016/02/11/hp-smart-array-cli-commands/
* https://h50146.www5.hpe.com/products/software/oe/linux/mainstream/support/doc/general/mgmt/ssa_cli/files/v240_130/hpssacli-2.40-13.0_help.txt
* https://unixlab.weebly.com/raid-array.html
* https://hardforum.com/threads/hp-dl380p-gen8-p420i-controller-hbamode.1852528/

### addendum (output from ssacli show detailed config)
	
	=>ctrl all show config detail
	
	Smart Array P410i in Slot 0 (Embedded)
	   Bus Interface: PCI
	   Slot: 0
	   Serial Number: 5001438013631A40
	   Cache Serial Number: PBCDH0CRH0V0L0
	   Controller Status: OK
	   Hardware Revision: C
	   Firmware Version: 6.64-0
	   Rebuild Priority: Medium
	   Expand Priority: Medium
	   Surface Scan Delay: 15 secs
	   Surface Scan Mode: Idle
	   Parallel Surface Scan Supported: No
	   Queue Depth: Automatic
	   Monitor and Performance Delay: 60  min
	   Elevator Sort: Enabled
	   Degraded Performance Optimization: Disabled
	   Wait for Cache Room: Disabled
	   Surface Analysis Inconsistency Notification: Disabled
	   Post Prompt Timeout: 0 secs
	   Cache Board Present: True
	   Cache Status: OK
	   Cache Ratio: 25% Read / 75% Write
	   Drive Write Cache: Disabled
	   Total Cache Size: 0.5
	   Total Cache Memory Available: 0.4
	   No-Battery Write Cache: Disabled
	   Cache Backup Power Source: Capacitors
	   Battery/Capacitor Count: 1
	   Battery/Capacitor Status: OK
	   SATA NCQ Supported: True
	   Number of Ports: 2 Internal only
	   Encryption: Not Set
	   Driver Name: hpsa
	   Driver Version: 3.4.20
	   Driver Supports SSD Smart Path: True
	   PCI Address (Domain:Bus:Device.Function): 0000:05:00.0
	   Port Max Phy Rate Limiting Supported: False
	   Host Serial Number: USE135N52V
	   Sanitize Erase Supported: False
	   Primary Boot Volume: None
	   Secondary Boot Volume: None
	
	
	
	   HP SAS Expander Card at Port 2C, Box 1, OK
	
	      Power Supply Status: Not Redundant
	      Vendor ID: HP
	      Serial Number: RF15BP2689
	      Firmware Version: 2.10
	      Drive Bays: 24
	      Port: 2C
	      Box: 1
	      Location: Internal
	
	   Expander 250 
	      Device Number: 250
	      Firmware Version: 2.10
	      WWID: 5001438014526C66
	      Box: 1
	      Vendor ID: HP
	
	   HP SAS Expander Card SEP 248 
	      Device Number: 248
	      Firmware Version: 2.10
	      Hardware Revision: Rev C
	      WWID: 5001438014526C65
	      Box: 2
	      Vendor ID: HP
	      Model: HP SAS EXP Card
	
	   Physical Drives
	      physicaldrive 2C:1:4 (port 2C:box 1:bay 4, SATA SSD, 240 GB, OK)
	      physicaldrive 2C:1:3 (port 2C:box 1:bay 3, SATA SSD, 240 GB, OK)
	      physicaldrive 2C:1:2 (port 2C:box 1:bay 2, SAS HDD, 146 GB, OK)
	      physicaldrive 2C:1:1 (port 2C:box 1:bay 1, SAS HDD, 146 GB, OK)
	      physicaldrive 3C:1:6 (port 3C:box 1:bay 6, SAS HDD, 300 GB, OK)
	      physicaldrive 3C:1:5 (port 3C:box 1:bay 5, SAS HDD, 300 GB, OK)
	
	
	
	   HP SAS Expander Card at Port 4C, Box 2, OK
	
	      Power Supply Status: Not Redundant
	      Vendor ID: HP
	      Serial Number: RF15BP2689
	      Firmware Version: 2.10
	      Drive Bays: 24
	      Port: 4C
	      Box: 2
	      Location: Internal
	
	   Expander 250 
	      Device Number: 250
	      Firmware Version: 2.10
	      WWID: 5001438014526C66
	      Box: 1
	      Vendor ID: HP
	
	   HP SAS Expander Card SEP 248 
	      Device Number: 248
	      Firmware Version: 2.10
	      Hardware Revision: Rev C
	      WWID: 5001438014526C65
	      Box: 2
	      Vendor ID: HP
	      Model: HP SAS EXP Card
	
	   Physical Drives
	      None attached
	
	
	   Port Name: 1I
	         Port ID: 0
	         Port Connection Number: 0
	         SAS Address: 5001438013631A40
	         Port Location: Internal
	
	   Port Name: 2I
	         Port ID: 1
	         Port Connection Number: 1
	         SAS Address: 5001438013631A44
	         Port Location: Internal
	
	   Array: A
	      Interface Type: SAS
	      Unused Space: 6 MB (0.00%)
	      Used Space: 273.40 GB (100.00%)
	      Status: OK
	      Array Type: Data 
	      Smart Path: disable
	
	
	      Logical Drive: 1
	         Size: 136.70 GB
	         Fault Tolerance: 1
	         Heads: 255
	         Sectors Per Track: 32
	         Cylinders: 35132
	         Strip Size: 256 KB
	         Full Stripe Size: 256 KB
	         Status: OK
	         Unrecoverable Media Errors: None
	         Caching:  Enabled
	         Unique Identifier: 600508B1001CAA24339C082CBF1B0912
	         Disk Name: /dev/sda 
	         Mount Points: / 80.0 GB Partition Number 2
	         OS Status: LOCKED
	         Logical Drive Label: A0E0B9A75001438013631A40256F
	         Mirror Group 1:
	            physicaldrive 2C:1:2 (port 2C:box 1:bay 2, SAS HDD, 146 GB, OK)
	         Mirror Group 2:
	            physicaldrive 2C:1:1 (port 2C:box 1:bay 1, SAS HDD, 146 GB, OK)
	         Drive Type: Data
	         LD Acceleration Method: Controller Cache
	
	
	      physicaldrive 2C:1:1
	         Port: 2C
	         Box: 1
	         Bay: 1
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: SAS
	         Size: 146 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Rotational Speed: 15000
	         Firmware Revision: HPDD
	         Serial Number: PLWGTWSE
	         WWID: 5000CCA00B53489D
	         Model: HP      EH0146FARWD
	         Current Temperature (C): 35
	         Maximum Temperature (C): 42
	         PHY Count: 2
	         PHY Transfer Rate: 6.0Gbps, Unknown
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	      physicaldrive 2C:1:2
	         Port: 2C
	         Box: 1
	         Bay: 2
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: SAS
	         Size: 146 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Rotational Speed: 15000
	         Firmware Revision: HPDD
	         Serial Number: PLWP0XNE
	         WWID: 5000CCA00B5E9B11
	         Model: HP      EH0146FARWD
	         Current Temperature (C): 34
	         Maximum Temperature (C): 47
	         PHY Count: 2
	         PHY Transfer Rate: 6.0Gbps, Unknown
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	
	
	   Array: B
	      Interface Type: Solid State SATA
	      Unused Space: 2 MB (0.00%)
	      Used Space: 223.54 GB (100.00%)
	      Status: OK
	      Array Type: Data 
	      Smart Path: disable
	
	
	      Logical Drive: 2
	         Size: 223.54 GB
	         Fault Tolerance: 0
	         Heads: 255
	         Sectors Per Track: 32
	         Cylinders: 57450
	         Strip Size: 256 KB
	         Full Stripe Size: 256 KB
	         Status: OK
	         Caching:  Enabled
	         Unique Identifier: 600508B1001CC841DD71B0E330404FF4
	         Disk Name: /dev/sdb 
	         Mount Points: None
	         Logical Drive Label: ABABB8965001438013631A40D1E0
	         Drive Type: Data
	         LD Acceleration Method: Controller Cache
	
	
	      physicaldrive 2C:1:3
	         Port: 2C
	         Box: 1
	         Bay: 3
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: Solid State SATA
	         Size: 240 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Firmware Revision: Q0410A
	         Serial Number: AB20180827A0101371
	         WWID: 5001438014526C41
	         Model: ATA     TEAML5Lite3D240G
	         SATA NCQ Capable: True
	         SATA NCQ Enabled: True
	         SSD Smart Trip Wearout: Not Supported
	         PHY Count: 1
	         PHY Transfer Rate: 3.0Gbps
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	
	
	   Array: C
	      Interface Type: Solid State SATA
	      Unused Space: 2 MB (0.00%)
	      Used Space: 223.54 GB (100.00%)
	      Status: OK
	      Array Type: Data 
	      Smart Path: disable
	
	
	      Logical Drive: 3
	         Size: 223.54 GB
	         Fault Tolerance: 0
	         Heads: 255
	         Sectors Per Track: 32
	         Cylinders: 57450
	         Strip Size: 256 KB
	         Full Stripe Size: 256 KB
	         Status: OK
	         Caching:  Enabled
	         Unique Identifier: 600508B1001CD1056D9358D036DE54EB
	         Disk Name: /dev/sdc 
	         Mount Points: None
	         Logical Drive Label: ABAB89005001438013631A4045F6
	         Drive Type: Data
	         LD Acceleration Method: Controller Cache
	
	
	      physicaldrive 2C:1:4
	         Port: 2C
	         Box: 1
	         Bay: 4
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: Solid State SATA
	         Size: 240 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Firmware Revision: Q0410A
	         Serial Number: AB20180827A0100293
	         WWID: 5001438014526C40
	         Model: ATA     TEAML5Lite3D240G
	         SATA NCQ Capable: True
	         SATA NCQ Enabled: True
	         SSD Smart Trip Wearout: Not Supported
	         PHY Count: 1
	         PHY Transfer Rate: 3.0Gbps
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	
	
	   Array: D
	      Interface Type: SAS
	      Unused Space: 0 MB (0.00%)
	      Used Space: 279.37 GB (100.00%)
	      Status: OK
	      Array Type: Data 
	      Smart Path: disable
	
	
	      Logical Drive: 4
	         Size: 279.37 GB
	         Fault Tolerance: 0
	         Heads: 255
	         Sectors Per Track: 32
	         Cylinders: 65535
	         Strip Size: 256 KB
	         Full Stripe Size: 256 KB
	         Status: OK
	         Caching:  Enabled
	         Unique Identifier: 600508B1001C868C26439B55D426224F
	         Disk Name: /dev/sdd 
	         Mount Points: None
	         Logical Drive Label: ABAB99875001438013631A40A72E
	         Drive Type: Data
	         LD Acceleration Method: Controller Cache
	
	
	      physicaldrive 3C:1:5
	         Port: 3C
	         Box: 1
	         Bay: 5
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: SAS
	         Size: 300 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Rotational Speed: 10000
	         Firmware Revision: HPD6 (FW update is recommended to minimum version: HPD7)
	         Serial Number: PQJ0EM4B
	         WWID: 5000CCA025718881
	         Model: HP      EG0300FBDBR
	         Current Temperature (C): 31
	         Maximum Temperature (C): 44
	         PHY Count: 2
	         PHY Transfer Rate: 6.0Gbps, Unknown
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	
	
	   Array: E
	      Interface Type: SAS
	      Unused Space: 0 MB (0.00%)
	      Used Space: 279.37 GB (100.00%)
	      Status: OK
	      Array Type: Data 
	      Smart Path: disable
	
	
	      Logical Drive: 5
	         Size: 279.37 GB
	         Fault Tolerance: 0
	         Heads: 255
	         Sectors Per Track: 32
	         Cylinders: 65535
	         Strip Size: 256 KB
	         Full Stripe Size: 256 KB
	         Status: OK
	         Caching:  Enabled
	         Unique Identifier: 600508B1001C380646CF15536E61E692
	         Disk Name: /dev/sde 
	         Mount Points: None
	         Logical Drive Label: ABABE9D05001438013631A4088C8
	         Drive Type: Data
	         LD Acceleration Method: Controller Cache
	
	
	      physicaldrive 3C:1:6
	         Port: 3C
	         Box: 1
	         Bay: 6
	         Status: OK
	         Drive Type: Data Drive
	         Interface Type: SAS
	         Size: 300 GB
	         Drive exposed to OS: False
	         Logical/Physical Block Size: 512/512
	         Rotational Speed: 10000
	         Firmware Revision: HPD6 (FW update is recommended to minimum version: HPD7)
	         Serial Number: PMVJ07DB
	         WWID: 5000CCA0211D1B55
	         Model: HP      EG0300FBDBR
	         Current Temperature (C): 31
	         Maximum Temperature (C): 57
	         PHY Count: 2
	         PHY Transfer Rate: 6.0Gbps, Unknown
	         Sanitize Erase Supported: False
	         Shingled Magnetic Recording Support: None
	
	
	   Expander 250 
	      Device Number: 250
	      Firmware Version: 2.10
	      WWID: 5001438014526C66
	      Box: 1
	      Vendor ID: HP
	
	   Expander 250 
	      Device Number: 250
	      Firmware Version: 2.10
	      WWID: 5001438014526C66
	      Box: 1
	      Vendor ID: HP
	
	   HP SAS Expander Card SEP 248 
	      Device Number: 248
	      Firmware Version: 2.10
	      Hardware Revision: Rev C
	      WWID: 5001438014526C65
	      Box: 2
	      Vendor ID: HP
	      Model: HP SAS EXP Card
	
	   HP SAS Expander Card SEP 248 
	      Device Number: 248
	      Firmware Version: 2.10
	      Hardware Revision: Rev C
	      WWID: 5001438014526C65
	      Box: 2
	      Vendor ID: HP
	      Model: HP SAS EXP Card
	
	   SEP (Vendor ID PMCSIERA, Model  SRC 8x6G) 249 
	      Device Number: 249
	      Firmware Version: RevC
	      WWID: 5001438013631A4F
	      Vendor ID: PMCSIERA
	      Model: SRC 8x6G
	