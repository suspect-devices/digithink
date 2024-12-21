#!/bin/bash
# update.sh for debian/ubuntu/centos/suse  (copyleft) don@suspecdevices.com
echo --------------------- begin updating `uname -n` ----------------------
if [ -x "$(command -v apt-get)" ]; then
   apt-get update
   apt-get -y dist-upgrade
   apt-get -y autoremove
fi
if  [ -x "$(command -v yum)" ]; then
   echo yum upgrade.
   yum -y upgrade
fi
if  [ -x "$(command -v pihole)" ]; then
   echo pihole upgrade.
   pihole -up
fi
if  [ -x "$(command -v zypper)" ]; then
   echo zypper dist-upgrade.
   zypper -y dist-upgrade
fi
echo ========================== done ==============================

