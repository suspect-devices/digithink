# Rocky Linux 8.4 LXD host. (AOC2024 install)

If Ubuntu's adoption of LXD and ZFS and other innovations are to mean anything they have to be separated from both debian (its technical underpinnings) and canonical (its "freindly" commercial counterpart). The rpm based world has been completely screwed over by Redhat refusing to allow a downstream open source to use them as a standard. This has created the disaster that is fedora 2xx and the longest officially supported operating system ever centos 7 at proposed 12 !@#$#!!!#@ years. Redhats choice to ditch centos 8 (which sucked as bad as redhats upstream afik) and use the open source community to beta test their new os could be found in the dictionary under Trumpery. While bs2020 the candiate and kb2018 our Governer have served us well for the last few years its time for something new. Something community sourced, smart, and revolutionary. 

It is our intention to support the community as it tells Red hat to fuck off while insuring that debian and ubuntus innovations do not go to waste. Therefore our new server is AOC20204 It will run Rocky Linux to create a robust and flexible server that would be perfectly at home on Ubuntu. 

Goals.

* Take advantage of Rocky Linux's downstream compatibility with RHEL8
  * Dell's support for its hardware is limited to commercial operating systems.
  *attempting to get their tools (raid configuration etc) wedged into ubuntu is like needing a root canal.*
* Use the tools that Ubuntu has been correctly supporting for virtualization.
  * LXD for both qemu VMs and lxc based containers.
  * zfs -- cause it just fucking rules.
* Leave our comfort zones.
  * and still do production quality work.
* Hetrogenaity (look it up on the interbutts).

## Minimal Viable Product.
In our environment Bernie's primary function has been to provide a fallback to Kate's solid work. It has been our playground and our backup server. At a minimum the new server needs to provide an LXD server to test and backup our production containers and virtual machines. As a refence we will start [here](https://docs.rockylinux.org/guides/lxd_server/).

The plan.

There are several factors that we won't be able to consider until we are actually on the box. Like hether or not the ssd's will work with the old percs.



1. Export images for ernest and the vm's teddy, and franklin.
2. Move teddy to kb2018
3. Pull the existing disks from bs2020.
4. Put the ssds into the first two bays and configure the perc to make a single mirrored disk
5. Install rocky linux 8.4 from an iso a dvd or a thumb drive.
6. BLDGP at [https://docs.rockylinux.org/guides/lxd_server/](https://docs.rockylinux.org/guides/lxd_server/)
7. Configure/test lxd networking
8. Copy profiles and images from kb2018
8. Migrate teddy to its new home.
9. Pull archive disk and mount replacement.

### References
* https://fatmin.com/2019/11/23/installing-rhel-8-1-on-dell-r710-r610-with-h700-raid-controller/
* https://docs.rockylinux.org/guides/lxd_server/
