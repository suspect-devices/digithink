# Fast Forward
Installing Debian packages from newer/previous distributionsOne of the compromises made in Ubuntu's long term support release cycle is that stability is preferred over features. This is usually a good thing however sometimes you need features that are only found in a future release. Two examples of this are trac-1.2.2 which has a working git integration, which is broken in 18.04's version ( trac-1.2 ). Another is GNUCobol's "Stable" version (2.2). 

## Manual installation
For trac, I pulled the package file from 18.10's repositories and installed it manually. 
This breaks any updates or security fixes that are made to the newer repository, as well as the base ones. I don't much care for this solution and won't map it out here. 

## Adding Future Repositories.

Adding future repositories to /etc/apt/sources allows us to pull from those repositories. 
	
	root@redshirt:~# nano /etc/apt/sources.list
	....
	deb http://archive.ubuntu.com/ubuntu/ disco restricted main multiverse universe
	deb http://archive.ubuntu.com/ubuntu/ disco-updates restricted main multiverse universe
	deb http://security.ubuntu.com/ubuntu/ disco-security restricted main multiverse universe
	

Unfortunately the newer repo now becomes the default repo for everything in it. Essentially, the next apt-get dist-upgrade will take your entire install to the bleeding edge. 

## Google sucks

_(AKA Following the instructions on https://medium.com/@george.shuklin/how-to-install-packages-from-a-newer-distribution-without-installing-unwanted-6584fa93208f)_
In addition to trying to get you to give your facebook or google credentials the top listed instructions on installing specific packages don't work. It did, however, provide clues.

More or less they tell you create the following file (somefile.pref) in /etc/apt/preferences.d/ and run apt-get update.
	
	Package: *
	Pin: release n=disco
	Pin-Priority: -10
	Package: gnucobol
	Pin: release n=disco
	Pin-Priority: 500
	
Following these instructions caused disco-security and disco-updates to have the same priority as the current release (bionic). 
	
	root@redshirt:~# nano /etc/apt/preferences.d/gnucobol22.pref
	...
	root@redshirt:~# apt-get update 
	...
	root@redshirt:~# apt-cache policy
	Package files:
	 100 /var/lib/dpkg/status
	     release a=now
	 500 http://security.ubuntu.com/ubuntu disco-security/universe amd64 Packages
	     release v=19.04,o=Ubuntu,a=disco-security,n=disco,l=Ubuntu,c=universe,b=amd64
	...
	
	 500 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages
	     release v=18.04,o=Ubuntu,a=bionic,n=bionic,l=Ubuntu,c=main,b=amd64
	     origin archive.ubuntu.com
	Pinned packages:
	     gnucobol -> 2.2-5 with priority 500
	
	
_That is NOT what we want. _

For instance, checking libc-bin shows that it would have installed from the new non LTS distribution.
	
	root@redshirt:~# apt-cache policy libc-bin
	libc-bin:
	  Installed: 2.27-3ubuntu1
	  Candidate: 2.29-0ubuntu2
	  Version table:
	     2.29-0ubuntu2 500
	        500 http://archive.ubuntu.com/ubuntu disco/main amd64 Packages
	 *** 2.27-3ubuntu1 500
	        500 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages
	        100 /var/lib/dpkg/status
	
	
Which would have likely wrecked havoc on system stability. _Good thing we are testing on a "redshirt"_
## Stepwise Refinement
Guessing there was no default we modified the file to be more specific like this. (This was incorrect default is actually 500 for packages that aren't installed)
	
	Package: *
	Pin: release n=bionic*
	Pin-Priority: 990
	
	Package: *
	Pin: release n=disco*
	Pin-Priority: -10
	
	Package: gnucobol
	Pin: release n=disco*
	Pin-Priority: 500
	
Which at least fixes some of the issues.
	
	root@redshirt:~# apt-cache policy
	Package files:
	 100 /var/lib/dpkg/status
	     release a=now
	 -10 http://security.ubuntu.com/ubuntu disco-security/universe amd64 Packages
	     release v=19.04,o=Ubuntu,a=disco-security,n=disco,l=Ubuntu,c=universe,b=amd64
	     origin security.ubuntu.com
	 ...     
	 -10 http://archive.ubuntu.com/ubuntu disco/restricted amd64 Packages
	     release v=19.04,o=Ubuntu,a=disco,n=disco,l=Ubuntu,c=restricted,b=amd64
	     origin archive.ubuntu.com
	 990 http://security.ubuntu.com/ubuntu bionic-security/multiverse amd64 Packages
	     release v=18.04,o=Ubuntu,a=bionic-security,n=bionic,l=Ubuntu,c=multiverse,b=amd64
	     origin security.ubuntu.com
	...
	 990 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages
	     release v=18.04,o=Ubuntu,a=bionic,n=bionic,l=Ubuntu,c=main,b=amd64
	     origin archive.ubuntu.com
	Pinned packages:
	     gnucobol -> 2.2-5 with priority 500
	
Which gets us close.
The stability is fixed.
	
	root@redshirt:~# apt-cache policy libc-bin
	libc-bin:
	  Installed: 2.27-3ubuntu1
	  Candidate: 2.27-3ubuntu1
	  Version table:
	     2.29-0ubuntu2 -10
	        -10 http://archive.ubuntu.com/ubuntu disco/main amd64 Packages
	 *** 2.27-3ubuntu1 990
	        990 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages
	        100 /var/lib/dpkg/status
	
But the dependencies for the new package aren't.
	
	root@redshirt:~# apt-get install --dry-run gnucobol
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	Some packages could not be installed. This may mean that you have
	requested an impossible situation or if you are using the unstable
	distribution that some required packages have not yet been created
	or been moved out of Incoming.
	The following information may help to resolve the situation:
	
	The following packages have unmet dependencies:
	 gnucobol : Depends: libcob4 but it is not installable
	            Depends: libcob4-dev (= 2.2-5) but it is not installable
	E: Unable to correct problems, you have held broken packages.
	root@redshirt:~# 
	
## RTFM _(man apt_preferences)_
The apt preferences man pages explain a tiered priority system where ranges of numbers determine apts' behavior. Setting the priority for future packages to 100 allows missing packages to be installed.
	
	root@redshirt:~# cat /etc/apt/preferences.d/gnucobol22.pref
	Package: *
	Pin: release n=bionic*
	Pin-Priority: 990
	
	Package: *
	Pin: release n=disco*
	Pin-Priority: 100
	
	Package: gnucobol
	Pin: release n=disco*
	Pin-Priority: 600
	
Which works as we intended.
	
	root@redshirt:~# apt-get update
	Hit:1 http://archive.ubuntu.com/ubuntu bionic InRelease
	Get:2 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
	Get:3 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]         
	Get:4 http://security.ubuntu.com/ubuntu disco-security InRelease [97.5 kB]                    
	Get:5 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]          
	Hit:6 http://archive.ubuntu.com/ubuntu disco InRelease         
	Fetched 350 kB in 2s (211 kB/s)                    
	Reading package lists... Done
	root@redshirt:~# apt-get install --dry-run gnucobol
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following additional packages will be installed:
	  binutils binutils-common binutils-x86-64-linux-gnu cpp cpp-7 gcc gcc-7 gcc-7-base libasan4 libatomic1 libbinutils libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libcob4
	  libcob4-dev libgcc-7-dev libgmp-dev libgmpxx4ldbl libgomp1 libisl19 libitm1 liblsan0 libmpc3 libmpx2 libncurses5-dev libncursesw6 libquadmath0 libtinfo-dev libtinfo6 libtsan0
	  libubsan0 linux-libc-dev manpages-dev
	Suggested packages:
	  binutils-doc cpp-doc gcc-7-locales gcc-multilib make autoconf automake libtool flex bison gdb gcc-doc gcc-7-multilib gcc-7-doc libgcc1-dbg libgomp1-dbg libitm1-dbg
	  libatomic1-dbg libasan4-dbg liblsan0-dbg libtsan0-dbg libubsan0-dbg libcilkrts5-dbg libmpx2-dbg libquadmath0-dbg glibc-doc gmp-doc libgmp10-doc libmpfr-dev ncurses-doc
	The following NEW packages will be installed:
	  binutils binutils-common binutils-x86-64-linux-gnu cpp cpp-7 gcc gcc-7 gcc-7-base gnucobol libasan4 libatomic1 libbinutils libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libcob4
	  libcob4-dev libgcc-7-dev libgmp-dev libgmpxx4ldbl libgomp1 libisl19 libitm1 liblsan0 libmpc3 libmpx2 libncurses5-dev libncursesw6 libquadmath0 libtinfo-dev libtinfo6 libtsan0
	  libubsan0 linux-libc-dev manpages-dev
	0 upgraded, 36 newly installed, 0 to remove and 3 not upgraded.
	Inst libtinfo6 (6.1+20181013-2ubuntu2 Ubuntu:19.04/disco [amd64])
	Inst libncursesw6 (6.1+20181013-2ubuntu2 Ubuntu:19.04/disco [amd64])
	Inst binutils-common (2.30-21ubuntu1~18.04.2 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libbinutils (2.30-21ubuntu1~18.04.2 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst binutils-x86-64-linux-gnu (2.30-21ubuntu1~18.04.2 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst binutils (2.30-21ubuntu1~18.04.2 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst gcc-7-base (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libisl19 (0.19-1 Ubuntu:18.04/bionic [amd64])
	Inst libmpc3 (1.1.0-1 Ubuntu:18.04/bionic, Ubuntu:19.04/disco [amd64])
	Inst cpp-7 (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst cpp (4:7.4.0-1ubuntu2.3 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libcc1-0 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libgomp1 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libitm1 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libatomic1 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libasan4 (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst liblsan0 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libtsan0 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libubsan0 (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libcilkrts5 (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libmpx2 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libquadmath0 (8.3.0-6ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libgcc-7-dev (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst gcc-7 (7.4.0-1ubuntu1~18.04.1 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst gcc (4:7.4.0-1ubuntu2.3 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libc-dev-bin (2.27-3ubuntu1 Ubuntu:18.04/bionic [amd64])
	Inst linux-libc-dev (4.15.0-54.58 Ubuntu:18.04/bionic-updates, Ubuntu:18.04/bionic-security [amd64])
	Inst libc6-dev (2.27-3ubuntu1 Ubuntu:18.04/bionic [amd64])
	Inst libgmpxx4ldbl (2:6.1.2+dfsg-2 Ubuntu:18.04/bionic [amd64])
	Inst libgmp-dev (2:6.1.2+dfsg-2 Ubuntu:18.04/bionic [amd64])
	Inst libtinfo-dev (6.1-1ubuntu1.18.04 Ubuntu:18.04/bionic-updates [amd64])
	Inst libncurses5-dev (6.1-1ubuntu1.18.04 Ubuntu:18.04/bionic-updates [amd64])
	Inst manpages-dev (4.15-1 Ubuntu:18.04/bionic [all])
	Inst libcob4 (2.2-5 Ubuntu:19.04/disco [amd64])
	Inst libcob4-dev (2.2-5 Ubuntu:19.04/disco [amd64])
	Inst gnucobol (2.2-5 Ubuntu:19.04/disco [amd64])
	Conf libtinfo6 (6.1+20181013-2ubuntu2 Ubuntu:19.04/disco [amd64])
	...
	Conf gnucobol (2.2-5 Ubuntu:19.04/disco [amd64])
	root@redshirt:~#
	
## References
* https://medium.com/@george.shuklin/how-to-install-packages-from-a-newer-distribution-without-installing-unwanted-6584fa93208f
* https://askubuntu.com/questions/49609/how-do-i-add-the-proposed-repository