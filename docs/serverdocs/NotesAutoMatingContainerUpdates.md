<!-- NotesAutoMatingContainerUpdates, Version: 1, Modified: 2018/12/02, Author: trac -->
#Notes: Automating Container Updates

This would have worked in an lxc only world...

	
	#!/bin/bash
	# Purpose: Update all lxc vms
	# Note: Tested on Ubuntu LTS only
	# Author: Vivek Gite <www.cyberciti.biz>, under GPL v2+
	# -------------------------------------------------------
	 
	# Get the vm list
	vms="$(lxc-ls --active)"
	 
	# Update each vm
	update_vm(){
	        local vm="$1"
	        echo "*** [VM: $vm [$(hostname) @ $(date)] ] ***"
	        /usr/bin/lxc-attach -n "$vm" apt-get -- -qq update
	        /usr/bin/lxc-attach -n "$vm" apt-get -- -qq -y upgrade
	        /usr/bin/lxc-attach -n "$vm" apt-get -- -qq -y clean
	        /usr/bin/lxc-attach -n "$vm" apt-get -- -qq -y autoclean 
	        # Note for RHEL/CentOS/Fedora Linux comment above two line and uncomment the following line #
	        # lxc-attach -n "$vm" yum -y update 
	        echo "-----------------------------------------------------------------"
	}
	 
	# Do it
	for v in $vms
	do
	   update_vm "$v"
	done
	

This works for updating everything debian under the lxd.. Not sure you need anything else :)
	
	#!/bin/bash
	# A simple shell script to update all lxd container hypervisor
	# URL: https://bash.cyberciti.biz/virtualization/shell-script-to-update-all-lxd-container-hypervisor/
	# Tested on : Ubuntu 16.04 LTS lxd server 
	# Tested on : Ubuntu/Debian lxd container hypervisor only 
	# ----------------------------------------------------------------------------
	# Author: nixCraft 
	# Copyright: 2016 nixCraft under GNU GPL v2.0+
	# ----------------------------------------------------------------------------
	# Last updated 14 Aug 2016
	# ----------------------------------------------------------------------------
	# Set full path to bins 
	_apt="/usr/bin/apt-get"
	_lxc="/usr/bin/lxc"
	_awk="/usr/bin/awk"
	
	# Get containers list
	clist="$(${_lxc} list -c ns | ${_awk} '!/NAME/{ if ( $4 == "RUNNING" ) print $2}')"
	
	# Use bash for loop and update all container hypervisor powered by Debian or Ubuntu
	# NOTE: for CentOS use yum command instead of apt-get
	for c in $clist
	do
		echo "Updating Debian/Ubuntu container hypervisor \"$c\"..."
		${_lxc} exec $c ${_apt} -- -qq update
		${_lxc} exec $c ${_apt} -- -qq -y upgrade
		${_lxc} exec $c ${_apt} -- -qq -y clean
		${_lxc} exec $c ${_apt} -- -qq -y autoclean
	done 
	

Shell Fragment for looking at os distribution. 
	
	# Determine OS platform
	UNAME=$(uname | tr "[:upper:]" "[:lower:]")
	# If Linux, try to determine specific distribution
	if [ "$UNAME" == "linux" ]; then
	    # If available, use LSB to identify distribution
	    if [ -f /etc/lsb-release -o -d /etc/lsb-release.d ]; then
	        export DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)
	    # Otherwise, use release info file
	    else
	        export DISTRO=$(ls -d /etc/[A-Za-z]*[_-][rv]e[lr]* | grep -v "lsb" | cut -d'/' -f3 | cut -d'-' -f1 | cut -d'_' -f1)
	    fi
	fi
	# For everything else (or if above failed), just use generic identifier
	[ "$DISTRO" == "" ] && export DISTRO=$UNAME
	unset UNAME
	
### Linkdump
* https://askubuntu.com/questions/459402/how-to-know-if-the-running-platform-is-ubuntu-or-centos-with-help-of-a-bash-scri
* https://ask.fedoraproject.org/en/question/49738/how-to-check-if-system-is-rpm-or-debian-based/
* http://fuckingshellscripts.org/
* https://etbe.coker.com.au/2007/08/30/identifying-the-distribution-of-a-linux-system/
* https://ask.fedoraproject.org/en/question/49738/how-to-check-if-system-is-rpm-or-debian-based/

* https://hvops.com/articles/ansible-vs-shell-scripts/
* https://news.ycombinator.com/item?id=6431552
* https://www.cyberciti.biz/faq/how-to-update-debian-or-ubuntu-linux-containers-lxc/
* https://blog.sleeplessbeastie.eu/2017/08/21/how-to-upgrade-lxd-guests/
* https://blog.selectel.com/managing-containers-lxd-brief-introduction/
* http://xmodulo.com/lxc-containers-ubuntu.html
