# Using a Tank for Crowd Control. -- DRAFT / Work In Progress --


Now that we [have our proof of concept](https://www.digithink.com/rethinkeverything/norouter/wireguard-and-tinyproxy/) We are going to reimpliment it using physical hardware and harden it. The idea is to access the Admin lan without giving it any more access than it needs. The admin land has the servers lights out interfaces (ilo and drac) and allows direct communication between servers.

## Hardware

Our router was originally designed to be used with pfsense, a comercial product built around freebsd and its packet filtering system.
![Sitka](./images/sitka.jpg)

At home we run opnsense which is an open source replacement. At the colo we are going to strip it down to its underlying operating system and open source compontents.


## Components

### Wireguard

(insert short description of wg) We originally set out to use several complicated vpns until we realized they were overkill.The configuration for wireguard is described in our [staging setup](https://www.digithink.com/rethinkeverything/norouter/wireguard-and-tinyproxy/)

### TinyProxy

The only reason the servers would need to directly connect to anything is to get updates. For this a simple http proxy is all that we need. The configuration for tinyproxy is described in our [staging setup](https://www.digithink.com/rethinkeverything/norouter/wireguard-and-tinyproxy/).


### Unbound

When talking to isolated internal machines its nice to have local dns.

### pf

Pf is bsd's packet filter system.

### Redundancy and remote control.


## References

- https://www.digithink.com/rethinkeverything/norouter/wireguard-and-tinyproxy/
- https://forums.freebsd.org/threads/wireguard-network-setup.94793/
- https://forums.freebsd.org/threads/wireguard-setup-with-pf-problems.72623/
- https://vlads.me/post/create-a-wireguard-server-on-freebsd-in-15-minutes/
- https://freebsdsoftware.org/www/tinyproxy.html