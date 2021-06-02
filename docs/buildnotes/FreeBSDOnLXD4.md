#FreeBSD on lxd
LXD 4.0 allows for the creation of VM's based on qemu. This allows us to create  "virtual machines" capable of running non linux operating systems such as FreeBSD (or god forbid WindBlows).

## Creating an empty vm.
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
I found that the console would not come up with the dual "Cons:" setting. Serial worked just fine.

### Linkdump.

* [https://forum.netgate.com/topic/154906/how-to-install-pfsense-on-lxc-vm-qemu](https://forum.netgate.com/topic/154906/how-to-install-pfsense-on-lxc-vm-qemu)
* [https://discuss.linuxcontainers.org/t/lxc-vm-running-freebsd-cant-see-hard-disk/8214/14](https://discuss.linuxcontainers.org/t/lxc-vm-running-freebsd-cant-see-hard-disk/8214/14)
* [https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-dvd1.iso](https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-dvd1.iso)
* [https://docs.freebsd.org/en/books/handbook/bsdinstall/#bsdinstall-start](https://docs.freebsd.org/en/books/handbook/bsdinstall/#bsdinstall-start)