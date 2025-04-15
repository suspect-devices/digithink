# Initial impression of opnsense
.

This is mostly a note about freebsd audit and why I went with opnsense. One of my coworkers didnt like some of the coding last time he looked at opnsense, but I am willing to ignore this while I work on being able to do most of this stuff by hand. 

## pkg audits and updates.
Out of the box pfsense-ce (2.6..) had over 20 vulnerabilities most of them in the core parts of the system. With an older version of freebsd and no real upgrade path I thought "well obscene me, this obscenes". This was really a deal breaker.

OPNsense on the other hand came out of the box with around a dozen which after a pgk update && pkg upgrade dropped down to one. This is recent, not critical and consistent with the upgrades I have been doing at work. Bodes well.

```
root@OPNsense:~ # pkg audit -F
vulnxml file up-to-date
py39-setuptools-63.1.0 is vulnerable:
  py39-setuptools -- denial of service vulnerability
  CVE: CVE-2022-40897
  WWW: https://vuxml.FreeBSD.org/freebsd/1b38aec4-4149-4c7d-851c-3c4de3a1fbd0.html

1 problem(s) in 1 installed package(s) found.
root@OPNsense:~ # freebsd-version
13.1-RELEASE-p5
```
## Link pile.

- https://forum.opnsense.org/index.php?topic=18274.0
- https://connortumbleson.com/2022/06/06/opnsense-wireguard-pihole/
- https://homegrowntechie.com/discovering-migrating-to-opnsense/