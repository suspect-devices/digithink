# <DEL>Rocky Linux 8.4</DEL> *Ubuntu 21.04 (Hirsute Hippo)* LXD host. (AOC2024 install)
*This was the best kind of fail*

While bs2020 the candiate and kb2018 our Governer have served us well for the last few years its time for something new. Something community sourced, smart, and revolutionary. AOC2024 


If Ubuntu's adoption of LXD and ZFS and other innovations are to mean anything they have to be separated from both debian (it's technical underpinnings) and Canonical (it's obnoxiously "freindly" commercial counterpart) or we will be captive to its "charms"[(1)](#fn1). Meanwhile, the rpm based world has been completely paralized by Redhat's inability or unwillingness to provide a downstream open source project to use as a standard. This has created the disaster that is fedora 2x and the longest currently supported linux operating system ever (Centos 7 at a proposed 12 years). Redhat's choice to ditch Centos 8 and use the open source community to beta test their new features can not be described politely [(2)](#fn2).

It <del>is</del>*was* our intention to support the community as it tells Redhat where to go while insuring that Debian and Ubuntu's innovations do not go to waste. Therefore, our new server <del>will run Rocky Linux</del> *will run the latest Ubuntu server release* to create a robust and flexible server which will compliment the work done by our Ubuntu LTS based server. 

## Goals.

* Take advantage of Rocky Linux's downstream *bug for bug* compatibility with RHEL8

    * Dell's support for its hardware is limited to commercial operating systems. *attempting to get their tools (raid, idrac, configuration etc) wedged into ubuntu is like needing a root canal.*

* Use the tools that Ubuntu/Canonical has been supporting for virtualization.

    * LXD for both VMs and lxc based containers.
    * zfs, cause it rules.

* Leave our comfort zones.

    * And still do production quality work.

* [heterogeneity](https://www.merriam-webster.com/dictionary/heterogeneity).

## Minimal Viable Product.
In our environment, Bernie's primary function has been to provide a fallback to Kate's solid work. It has been our playground and our backup server. At a minimum the new server needs to provide an LXD server to test and backup our production containers and virtual machines. As a refence <del>we will</del>*tried to* start at [Rocky Linux's LXD server guide](https://docs.rockylinux.org/guides/lxd_server/).

### The <del>original</del>*revised* plan.

There are several factors that we won't be able to consider until we are actually on the box. Like whether or not <del>the ssd's will work well with the old raid controller. </del> 
*The installer will find the disks presented by the raid controller.
The SSDs were fine, however Rocky is aptly named..*

1. Export images for ernest and the vm's teddy, and franklin.
2. Pull archive disk and mount it's replacement on kb2018.
3. Move teddy(dns2) to kb2018
4. Pull the existing disks from bs2020.
5. Put the ssds into the first two bays and configure the perc to make a single mirrored disk
6. <del> Install rocky linux 8.4 from an iso a dvd or a thumb drive.</del> *Install newest ubuntu release 21.04 (Hirsute Hippo)*
7. BLDGP[(3)](#fn3) at <del>[https://docs.rockylinux.org/guides/lxd_server/](https://docs.rockylinux.org/guides/lxd_server/)</del> *[the notes from the last lxd server we built](https://www.digithink.com/buildnotes/edge-server-configuration/) combined with a document that we havent written yet* 
8. Configure/test disks, lxd, and networking.
9. Copy profiles and images from kb2018
10. Add and configure ansible.
11. Migrate teddy to its new home.

### What actually happened.
1. We exported the images and the lxd configuration to the archive disk as described in [ticket: #79](https://serverdocs.suspectdevices.com/serverdocs/ticket/79) 
2. We unmounted the archive disk. 
3. We shutdown teddy and moved the container to kb2018
4. We pulled and labled all of the disks on bs2020
5. We installed two new 240G SSDs and two new 1TB 10K disks and configured the raid controller to make a raid 1 mirror of the ssds. (the bigger disks will be handled by zfs).
6. We attempted for several hours to install rocky linux 8.4 on the system but could not get the operating system to recognize any installable disks. So, knowing that we would need to adapt whatever changes Ubuntu threw at us in the spring, we installed the newest server release *[21.04 (Hirsute Hippo)](http://www.releases.ubuntu.com/21.04/)*
7. We updated and installed the prerequisites for lxd/w zfs.
8. We configured the network and disks needed to restore the lxd configuration.
9. We restored the lxd configuration from the archive disk.
10. We moved teddy back to the new lxd configuration.
11. We restored the spare containers from the archive disk.
12. Pulled the archive disk off sight.

### Todo:
1. Configure ansible on the new server [Ticket #81](https://serverdocs.suspectdevices.com/serverdocs/ticket/81)
2. Update backup scripts to reference new server.[Ticket #82](https://serverdocs.suspectdevices.com/serverdocs/ticket/82)
3. Make backup scripts work with vms [Ticket #58](https://serverdocs.suspectdevices.com/serverdocs/ticket/58)
4. Script archives to create new off site rotating disk.[Ticket #83](https://serverdocs.suspectdevices.com/serverdocs/ticket/83#ticket)

### References
* https://fatmin.com/2019/11/23/installing-rhel-8-1-on-dell-r710-r610-with-h700-raid-controller/
* https://docs.rockylinux.org/guides/lxd_server/

### Footnotes / Sarcasms
1. <a name=fn1></a>Snaps? Juju? Really???? 
2. <a name=fn2></a>See: [trumpery](https://www.lexico.com/en/definition/trumpery)
3. <a name=fn3></a>BLDGP/BLGDP = "Build it Like the Dad Gummed Plans". This is a reference to a 70s American Aircraft Modeler editorial on people building tri-planes out of plans for bi-planes and then wondering why they don't fly.


