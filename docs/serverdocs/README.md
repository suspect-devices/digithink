# Server Modernization

This is an ongoing project that hosts several domains. 

## Overview 

![](images/ContainerShip.jpg)

### Phase I (2017-2018)

Phase one of the server modernization shifted away from multipurposed servers and kvms to lxc/lxd based containers.

* Moving all legacy system functions onto separate linux containers isolated from each other.
* Use mirrored disk systems to insure that disk corruption does not lead to data corruption.
* Start giving a shit about the systems, code, and sites on them.
* Own your code/data. (If your free code hosting system is shutdown or taken over by Microsoft is it really free?)

### Server Modernization Phase II (2019-2021)

Phase two extends on this by integrate Ansible into system maintenance tasks.

* Integrate Ansible into system maintenance tasks
* Reevaluate Centos and other RPM based containers built using playbooks vs profiles/scripts/cloud-init *while maintaining current security model*
* Clean up the cruft (If it doesn't bring you joy DTMFA)

### SMP III Own Your Shit (2022-2023)

- Work on secure and efficient traffic in and out of home lans (Privoxy,DNS based ad blocking,squid etc)
- Continue to refine server operation/maintanance.
- Build out content.
  - [git to markdown automation](https://bartender.digithink.com)
- Rethink openwrt based routing.
  - explore opnsense
- [Document original home server/network setup](/zeearchive/edge-server-configuration/)
- [Rethink everything](/rethinkeverything/)

### SMP IV Keep going (2024-).
- Reduce colo footprint.
  - remove the dell.
- Dump Canonical
  - debian
  - incus
- Adapt Freebsd based firewall/router
  - wireguard
  - dnsmasq
  - pf

- Make shit happen
  - Build out content.
  - Start new projects.
  - Distribute data and backups over the network to home servers.

### Goals.

* Security
* Flexibility
* Simplification

### Isolation

* network
* performance
* disk

