# Stick a fork in them and turn them over they're done.
Recently we had to rebuild one of our servers because the hardware raided boot disk that had behaved perfectly for years shat on the bood disk. I tried to remotely (via ipmi/virtualized serial)install a zfs rooted ubuntu (24.04) I waisted 2 man weeks. Then I spent an entire weekend and more money than a surplus dell r7xx driving to the colo (6 hrs away) and installing it (desktop install converted to zfs/server because thats the only pathway provided only to have it implode when implimenting the mirrors. We finally (with remote hands) installed 24.04 server on a single disk but at this point I am was much done.

There are no polite words for the behaviour of Canonical with regards to sane headless installs with redundant root volumes. 

There are other issues to take up not the least of which is their destruction of LXD.

I think the last straw was how unfriendly and unhelpfull the #ubuntu chanel was. They used to be wrong but friendly.

# Stick a fork in them and turn them over they're done

YOU ARE HERE SUMMARIZING THE PLAN MOVING FORWARD

## Debian

Debian not only allowed me to install a system over a virtual serial console but allowed me to install from the original ubuntu. [Replaced ubuntu server with debian](https://www.digithink.com/rethinkeverything/no-canonical/debian/) (with a dual boot pathway back) on the secondary lxd server. Will migrate the containers on the main server to and repeat it with our primary server.

## Incus