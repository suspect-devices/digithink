# Openwrt build notes (er-lite3 v19.07.7)
*This build is based on our  [build of openwrt for the home lan.](https://bitbucket.org/houselan/config/src/master/)*

Since the er-lite uses a usb boot drive we are no longer constrained by the usual space restrictions. For that reason we have room to add python/ansible to managing this host. We still trim the os as much as possible in order to minimize the attack surfaces avalible to the wild.  (ipv6 and luci aren't needed here for instance)

### Objectives 
* pre-build os hardening.
* python3 for ansible management 
* wireguard
* ipv4 only
* git based configuration management (if possible)


### Changes since 19.07.3
* Somewhere since v19.07.3 the shadow password file has been rolled into the OS. *(So adduser instead of shadow_adduser add etc...)*.
* The built in logger conflicts with syslog_ng so I hope that means we can pipe our loggs off to another system.


## Pre hardening and initial configuration during build.
In our deployment the router is maintained externally. For this reason direct login to the router as root is disabled and sudo enabled accounts are installed. These accounts connect using ssh keys and escallate privilages with their passwords. The root account is locked and ssh access is allowed from the wan port. The process for this is documented [here](http://www.digithink.com/serverdocs/HardeningLEDE/)
This configuration is added to the build under the files directory where they are copied into the root filesystem of the target. The box then comes up pre configured and pre-hardened. One kludge used here is to add an rc.local which changes the users home directorys to be owned by them. Otherwise the ssh keys will not have the correct permissions. The files diretory is maintained in a [private git repository](https://bitbucket.org/suspectdevicesadmin/goodknight-configuration/src/master/).
Addiontally /etc/sudoers, /etc/rc.local, and /home are added to /etc/sysupgrade.conf in order to preserve them during sysupgrade.

### Changes made to the os.

* Added sudo admin accounts and locked the root account.
* Locked the console.
  The console out of the box is wide open normally that wouldnt be a problem since the serial ports on most routers aren't exposed. 
  
  ```
  # nano /etc/config/system
  ...	
  option ttylogin '1'
  ... 
  ```
  
* Added python3 and tested pip for future work
* Added and configured postfix as a satellite system
* removed symlink to /etc/resolv.conf 

  I have no idea why everyone has got to mess this up.
  
#### Additional packages
* sudo
* adduser
* nano, monit
* git, git-http
* postfix

### build history
```
git clone -b v19.07.7 https://github.com/openwrt/openwrt.git
cd openwrt
mv files /tmp/
git clone git@bitbucket.org:suspectdevicesadmin/goodknight-configuration.git files
cp files/lede19.07.7-erlite-ext4.diffconfig .config
make defconfig
./scripts/feeds update -a
./scripts/feeds install -a
make -j8 v=sc download world
mv bin/targets/octeon/generic/openwrt-octeon-erlite-ext4-sysupgrade.tar.gz ~/firmware/lede19.07.7-erlite-ext4.tgz
./scripts/diffconfig.sh >  ~/firmware/lede19.07.7-erlite-ext4.diffconfig
./scripts/diffconfig.sh >  files/lede19.07.7-erlite-ext4.diffconfig
cd files
git commit -a -m "update diffconfig in repo"
git push
```

### Link Dump
* [http://www.digithink.com/serverdocs/HardeningLEDE/](http://www.digithink.com/serverdocs/HardeningLEDE/)
* [https://oldwiki.archive.openwrt.org/doc/howto/serial.console.password](https://oldwiki.archive.openwrt.org/doc/howto/serial.console.password)
* [https://blog.suspectdevices.com/blahg/openwrt/lede-19-07-on-the-ubiquity-er-lite3/](https://blog.suspectdevices.com/blahg/openwrt/lede-19-07-on-the-ubiquity-er-lite3/)
