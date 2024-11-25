#FreeBSD on lxd
LXD 4.0 allows for the creation of VM's based on qemu. This allows us to create  "virtual machines" capable of running non linux operating systems such as FreeBSD (or god forbid WindBlows). So let's look at adding a freebsd 12.3 box to our setup.

## Create an empty vm.
Based on the examples I was able to find we start by creating an empty vm and then tweek on a few of the parameters (raw.apparmor and raw.qemu). While there i adjust the nic (I am sure that all of this could be done on the init line). After that it's pretty straight forward.

```
root@bs2020:/home/feurig# lxc init henry --empty --vm -c limits.cpu=4 -c limits.memory=4GB -c security.secureboot=false -n br0
Creating henry
root@bs2020:/home/feurig# lxc config device add henry install disk source=/home/feurig/FreeBSD-12.2-RELEASE-amd64-dvd1.iso
Device install added to henry
root@bs2020:/home/feurig# lxc config edit henry 
architecture: x86_64
config:
  limits.cpu: "4"
  limits.memory: 4GB
  security.secureboot: "false"
  ## tweek apparmor/qemu settings
  raw.apparmor: /home/feurig/** rwk,
  raw.qemu: -boot menu=on -machine pc-q35-2.6
  volatile.apply_template: create
  volatile.br0.hwaddr: 00:16:3e:ab:07:4e
  volatile.eth0.hwaddr: 00:16:3e:87:3c:b1
devices:
  eth0:
    nictype: bridged
    parent: br0
    type: nic
ephemeral: false
profiles:
- default
stateful: false
description: "FreeBSD 12.3 test box"
root@bs2020:/home/feurig# lxc start henry --console
   ______               ____   _____ _____  
  |  ____|             |  _ \ / ____|  __ \ 
  | |___ _ __ ___  ___ | |_) | (___ | |  | |
  |  ___| '__/ _ \/ _ \|  _ < \___ \| |  | |
  | |   | | |  __/  __/| |_) |____) | |__| |
  | |   | | |    |    ||     |      |      |
  |_|   |_|  \___|\___||____/|_____/|_____/ 
                                                 ```                        `
 ????????????Welcome to FreeBSD?????????????    s` `.....---.......--.```   -/
 ?                                         ?    +o   .--`         /y:`      +.
 ?  1. Boot Multi user [Enter]             ?     yo`:.            :o      `+-
 ?  2. Boot Single user                    ?      y/               -/`   -o/
 ?  3. Escape to loader prompt             ?     .-                  ::/sy+:.
 ?  4. Reboot                              ?     /                     `--  /
 ?  5. Cons: Serial                        ?    `:                          :`
 ?                                         ?    `:                          :`
 ?  Options:                               ?     /                          /
 ?  6. Kernel: default/kernel (1 of 1)     ?     .-                        -.
 ?  7. Boot Options                        ?      --                      -.
 ?                                         ?       `:`                  `:`
 ?                                         ?         .--             `--.
 ???????????????????????????????????????????            .---.....----.

```
I found that, on at least one of my servers, the console would not come up with the dual "Cons:" setting. Serial worked just fine.

## Next Steps (sudo, ssh, hardening, usw)

In order to have the server play well with our environment I install the following packages using pkg (sudo, nano, bash, bash-completion, python37) as well as manually adding admin users. At some point it would be nice to use cloud-init or if that is unworkable ansible for the initial configuration.

```.
[root@henry /usr/home/feurig]# pkg info
bash-5.1.4_1                   GNU Project's Bourne Again SHell
bash-completion-2.11,2         Programmable completion library for Bash
gettext-runtime-0.21           GNU gettext runtime libraries and programs
indexinfo-0.3.1                Utility to regenerate the GNU info page index
libffi-3.3_1                   Foreign Function Interface
nano-5.5                       Nano's ANOther editor, an enhanced free Pico clone
pkg-1.16.3                     Package manager
py37-pip-20.2.3                Tool for installing and managing Python packages
py37-setuptools-44.0.0         Python packages installer
python37-3.7.10                Interpreted object-oriented programming language
readline-8.1.0                 Library for editing command lines as they are typed
sudo-1.9.6p1                   Allow others to run commands as root
```
Nano and bash are a personal preference of mine.

```
feurig@henry:~ $ sudo bash
Password:
[root@henry /usr/home/feurig]# chpass -s /usr/local/bin/bash feurig
[root@henry /usr/home/feurig]# chpass -s /usr/local/bin/bash joe

```

## Setting up Ansible on BSD

In addition to installing python ssh and an admin user needs to be set up as lxd does not "lxc exec" directly to virtual machines. 

```
[root@henry /usr/home/feurig]# visudo 
... comment out this 
 # root ALL=(ALL) ALL
... and uncomment out this
%wheel ALL=(ALL) ALL
...
[root@henry /usr/home/feurig]# adduser ansible
... add ansible to wheel group ...
[root@henry /usr/home/feurig]# su - ansible
ansible@henry:~ $ssh-keygen
ansible@henry:~ $cat >> .ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCssxhi6P1Ssin8QjEMlm+9W1L5ncRqejnw78z/yhQLwCU2av3+vAzPFDKi7CTm2iqeRoNYsKx4IaNYK9t+zQ0OsEXjzIzS+uCNODbNaW4pMtaHcwsaYDCdG9OiXuFa7qWndDAvSJjXQR6t1pygdw/tdbsGN0//zq71j9ChitXJQUr0YYCYwa4MaB6Srn/Zpkhfut1OP56XMo15F+0YD+oS/IqJp/QTH6Q9LzVh+HKI9rdhDEqEsrNZsaQw6UZ8JrfRYmJWzcFlqztv2qBv/BdStWbJGMBDTDNOSqf9wkts43lkZGYgSyZo80NLmq4oXJanuNO0wOBeRtMyX+HUEmgh root@kb2018
<ctrl-D>
``` 

Adding the become password to the ansible servers vault is described [here](https://www.digithink.com/buildnotes/ansible/ServerInstall/)

## Adding an update.sh script.
### The field expedient way

For quick and dirty's sake we add the following to /usr/local/bin/update.sh which could easily be added to the generalized shell since we have decided that bash is ok. It also might be ok to check if a reboot is necissary.

```
[root@henry /usr/home/feurig]# cat /usr/local/bin/update.sh 
#!/bin/sh
freebsd-update fetch install
pkg upgrade
```
And then life is good and our new pets are equally loved. (including the centos 7 result for sag)

```
root@kb2018:/etc/ansible/python# ansible pets -m raw -a "update.sh"
shelly | CHANGED | rc=0 >>
...
henry | CHANGED | rc=0 >>

src component not installed, skipped
Looking up update.FreeBSD.org mirrors... 2 mirrors found.
Fetching metadata signature for 12.2-RELEASE from update1.freebsd.org... done.
Fetching metadata index... done.
Inspecting system... done.
Preparing to download files... done.

No updates needed to update system to 12.2-RELEASE-p8.
No updates are available to install.
Updating FreeBSD repository catalogue...
FreeBSD repository is up to date.
All repositories are up to date.
Checking for upgrades (1 candidates): 100%
Processing candidates (1 candidates): 100%
Checking integrity... done (0 conflicting)
Your packages are up to date.
Shared connection to henry closed.

keynes | CHANGED | rc=0 >>
--------------------- begin updating keynes ----------------------
yum upgrade.
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.cat.pdx.edu
 * extras: mirror.web-ster.com
 * updates: mirror.keystealth.org
No packages marked for update
========================== done ==============================
Failed to set locale, defaulting to C
...
naomi | CHANGED | rc=0 >>
--------------------- begin updating naomi ----------------------
Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Hit:2 http://archive.ubuntu.com/ubuntu bionic InRelease
```

### Making it right.
Once we make peace with installing/enforcing bash on a freebsd box then we can add the freebsd update to our multi platform [update.sh](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/files/update.sh) (again someday deployed by lxd/cloud-init). 

```
[root@henry /usr/home/feurig]# ln -s /usr/local/bin/bash /bin/
[root@henry /usr/home/feurig]# nano /usr/local/bin/update.sh 
#!/bin/bash
# update.sh for debian/ubuntu/centos/suse/freebsd/pihole
# https://bitbucket.org/suspectdevicesadmin/ansible/src/master/files/update.sh
# (copyleft 2021) don@suspecdevices.com
echo --------------------- begin updating `uname -n` ----------------------
if [ -x "$(command -v apt-get)" ]; then
   echo Updating system
   apt-get update
   apt-get -y dist-upgrade
   apt-get -y autoremove
fi
if  [ -x "$(command -v yum)" ]; then
   echo yum upgrade.
   yum -y upgrade
fi
if  [ -x "$(command -v pihole)" ]; then
   echo Updating pihole.
   pihole -up
fi
if  [ -x "$(command -v zypper)" ]; then
   echo zypper dist-upgrade.
   zypper -y dist-upgrade
fi
if [ -x "$(command -v freebsd-update)" ]; then
   echo Updating freebsd base
   freebsd-update fetch install
   echo Updating freebsd packages
   pkg upgrade
fi
echo ========================== done ==============================
```

## To do.
* Look at restricting ansibles ssh access to hosts on the admin lan (as is done for bs2020).
* Add virtual machines to nightly backups (currently only containers).

```
root@kb2018:/# lxc snapshot henry 2021-06-05
root@kb2018:/# lxc move henry/2021-06-05 bs2020:Spare-henry-2021-06-05
root@kb2018:/# lxc stop bs2020:Spare-henry-2021-06-05
Error: The instance is already stopped
```

### Linkdump.

* [https://forum.netgate.com/topic/154906/how-to-install-pfsense-on-lxc-vm-qemu](https://forum.netgate.com/topic/154906/how-to-install-pfsense-on-lxc-vm-qemu)
* [https://discuss.linuxcontainers.org/t/lxc-vm-running-freebsd-cant-see-hard-disk/8214/14](https://discuss.linuxcontainers.org/t/lxc-vm-running-freebsd-cant-see-hard-disk/8214/14)
* [https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-dvd1.iso](https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-dvd1.iso)
* [https://docs.freebsd.org/en/books/handbook/bsdinstall/#bsdinstall-start](https://docs.freebsd.org/en/books/handbook/bsdinstall/#bsdinstall-start)