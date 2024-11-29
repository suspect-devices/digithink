<!-- NotesAutoMatingContainerUpdates, Version: 1, Modified: 2018/12/02, Author: trac -->
# Notes: Automating Container Updates

This would have worked in an lxc only world...

```sh
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
```

This works for updating everything debian under the lxd.. Not sure you need anything else :)
	

```sh
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
```

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
