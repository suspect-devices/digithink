# Reconsidering OpnSense

My initial tact was to take opnsense and use it as a prototype for the underlying freebsd based software (pf,dnsmasq,usw)
That is the configuration at the colo and it works well in that environment. However recently I started looking at what opnsense out of the box brings to the table. In particular I started looking at the total pile of shit that my centurylink provided router was letting into my network. And I decided that if I was hand rolling pf I would not have caught half of it.

I was in the middle of converting everything to /etc/ethers+/etc/hosts+dnsmasq and I said heck, lets just do the same in opnsense. Then we can look at getting rid of the pile of hot garbage that centurylink is charging me $15 a month for. 

## Well. That didn't work

So I turned on the dnsmasq dns and added all of the hosts in my network to /etc/hosts and /etc/ethers It seemed to work but the next time I did an update it overwrote both files, and stopped resolving the hosts I used most. So the main takaways were.

1. It seems to work at first.
2. It overwrites your files.
3. You have to manually add everything using the gui.
4. It's not automatable or scriptable.
5. It doesn't work.

So I turned unbound back on and looked at the alternatives.

## You can't configure the software/services but you can run a jail.

So this is going to be a longer process than I would have liked.

### installing a freebsd jail on an opnsense server

EINFACH. ZB.

```sh
curl http://ftp.uk.freebsd.org/pub/FreeBSD/releases/amd64/14.3-RELEASE/base.txz --output 14.3-RELEASE.base.tgz
ls
cd /jails/
tar -xJpf ~root/14.3-RELEASE.base.tgz  -C figaro/
ls
nano figaro/etc/rc.conf
cp -pv /etc/resolv.conf figaro/etc/
freebsd-update -b figaro/ fetch install
cat >/etc/jail.conf<<EOD
interface = igb0;
path = /jails/${name};
host.hostname = "${name}";
exec.consolelog = "/var/log/jail_console_${name}.log";
exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
exec.jail_user = root;
allow.raw_sockets;
allow.mount;
allow.mount.zfs;
enforce_statfs = 1;
mount.devfs;

figaro {
ip4.addr = "192.168.128.2";
}
EOD
service jail start figaro
```

 As for what to do with the jail. I am going to have to separate the documentaion for how I want to drive dnsmasq and how its configured since most of the configuation will be in a host repo.

 YOU ARE HERE LINKING TO THE DNSMASQ CONFIGURATION ON THE JAIL.

## Linkdump

- https://github.com/exeba/FTL-freebsd-port/blob/main/examples/jail-setup.sh
- https://forum.opnsense.org/index.php?topic=26975.0
- https://www.reddit.com/r/opnsense/comments/sjewa4/jails_under_opnsense_221/?rdt=59758
- https://forum.opnsense.org/index.php?topic=26724.0
