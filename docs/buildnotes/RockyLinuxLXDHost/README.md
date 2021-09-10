# Rocky Linux 8.4 LXD host. (AOC2024 install)
While bs2020 the candiate and kb2018 our Governer have served us well for the last few years its time for something new. Something community sourced, smart, and revolutionary. AOC2024 


If Ubuntu's adoption of LXD and ZFS and other innovations are to mean anything they have to be separated from both debian (its technical underpinnings) and canonical (it's obnoxiously "freindly" commercial counterpart) or we will be captive to its "charms"[(1)](#fn1). Meanwhile rpm based world has been completely paralized by Redhat's inability or unwillingness to provide a downstream open source project to use as a standard. This has created the disaster that is fedora 2xx and the longest officially supported linux operating system ever (centos 7 at a proposed 12 years). Redhats choice to ditch centos 8 and use the open source community to beta test their new features can not be described politely [(2)](#fn2).

It is our intention to support the community as it tells Red hat where to go while insuring that debian and ubuntus innovations do not go to waste. Therefore our new server will run Rocky Linux to create a robust and flexible server which will compliment the work done by our Ubuntu LTS based server. 

Goals.

* Take advantage of Rocky Linux's downstream compatibility with RHEL8

    * Dell's support for its hardware is limited to commercial operating systems. *attempting to get their tools (raid, idrac, configuration etc) wedged into ubuntu is like needing a root canal.*

* Use the tools that Ubuntu has been supporting for virtualization.

    * LXD for both qemu VMs and lxc based containers.
    * zfs -- cause it rules.

* Leave our comfort zones.

    * And still do production quality work.

* Hetrogenaity (look it up on the interbutts).

## Minimal Viable Product.
In our environment Bernie's primary function has been to provide a fallback to Kate's solid work. It has been our playground and our backup server. At a minimum the new server needs to provide an LXD server to test and backup our production containers and virtual machines. As a refence we will start at [Rocky Linux's LXD server guide](https://docs.rockylinux.org/guides/lxd_server/).

The plan.

There are several factors that we won't be able to consider until we are actually on the box. Like whether or not the ssd's will work well with the old percs.

1. Export images for ernest and the vm's teddy, and franklin.
2. Pull archive disk and mount it's replacement on kb2018.
3. Move teddy(dns2) to kb2018
4. Pull the existing disks from bs2020.
5. Put the ssds into the first two bays and configure the perc to make a single mirrored disk
6. Install rocky linux 8.4 from an iso a dvd or a thumb drive.
7. BLDGP[(3)](#fn3) at [https://docs.rockylinux.org/guides/lxd_server/](https://docs.rockylinux.org/guides/lxd_server/)
8. Configure/test lxd networking
9. Copy profiles and images from kb2018
10. Migrate teddy to its new home.

### References
* https://fatmin.com/2019/11/23/installing-rhel-8-1-on-dell-r710-r610-with-h700-raid-controller/
* https://docs.rockylinux.org/guides/lxd_server/

### Footnotes / Sarcasms
1. <a name=fn1></a> Snaps? Juju? Really???? 
2. <a name=fn2></a>See: [trumpery](https://www.lexico.com/en/definition/trumpery)
3. <a name=fn3></a>BLDGP/BLGDP = "Build it Like the Dad Gummed Plans". This is a reference to a 70s American Aircraft Moddler editorial on people building tri-planes out of plans for bi-planes and then wondering why they don't fly.
