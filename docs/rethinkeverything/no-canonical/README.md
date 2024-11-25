# Stick a fork in them and turn them over they're done
Recently we had to rebuild one of our servers because the hardware raided boot disk that had behaved perfectly for years shat on the bood disk. I tried to remotely (via ipmi/virtualized serial)install a zfs rooted ubuntu (24.04) I waisted 2 man weeks. Then I spent an entire weekend and more money than a surplus dell r7xx driving to the colo (6 hrs away) and installing it (desktop install converted to zfs/server because thats the only pathway provided only to have it implode when implimenting the mirrors. We finally (with remote hands) installed 24.04 server on a single disk but at this point I was very much done. After a over a decade of using ubuntu as my primary server operating system Canonical has driven it into the dirt.

There are no polite words for the behaviour of Canonical with regards to sane headless installs with redundant root volumes. 

There are other issues to take up not the least of which is their destruction of LXD.

I think the last straw was how unfriendly and unhelpfull the #ubuntu chanel was. They used to be wrong but friendly.

## No really (queue the intro to freaky styley) 

We are in the process of reducing our colo presence from 2 servers to one server and replacing our firewall. While there we will migrate from lxd to incus and then from Ubuntu to the underlying Debian. From there we will continue to migrate the containers running Ubuntu to Debian and other well behaved operating systems.

### Debian

In this particular use case, Debian not only allowed me to install a system over a virtual serial console but allowed me to install from the original ubuntu. [Replaced ubuntu server with debian](https://www.digithink.com/rethinkeverything/no-canonical/debian/) (with a temporary dual boot pathway back) on the secondary lxd server. Will migrate the containers on the main server to and repeat it with our primary server.


### Incus

Canonical really pooched the LXD service. First with its insistance of using snaps for everything, second by alienating its lead developers, and finally changing the licensing from an open source platform to a less permissive licence. There are no polite words.

So I am [migrating all of my lxd implimentations to the open source incus project](https://www.digithink.com/rethinkeverything/no-canonical/incus/).

## The plan

### Servers 

#### Test.(done) 
- Migrate non critical home lxd servers (utah/costello) to Debian. (done)
- Migrate lxd to incus on first two home servers. (done)
- Test incus to incus container migration.(done)

#### Repeat process at colocation 
- Migrate secondary server to debian/incus. (done)
- Migrate primary server to incus. (done)
- Move containers temporarily to secondary server.
- Migrate primary server to debian.
- Migrate containers back to primary.
- Down secondary server.

### Firewall/Router.
This work is described at [https://www.digithink.com/rethinkeverything/norouter/using-a-tank-for-crowd-control/](https://www.digithink.com/rethinkeverything/norouter/using-a-tank-for-crowd-control/)
- Set up wireguard (done)
- Set up secondary dns (done)
- Set up tinyproxy (done)
- Set up dnsmasq for admin lan.
- Harden the whole mess with pf.
