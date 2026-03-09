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
But somehow we have located a fellow traveler.

```sh
git clone https://github.com/exeba/FTL-freebsd-port.git
cd FTL-freebsd-port/examples/
nano jail-setup.sh
./jail-setup.sh
```

This is the current jail-setup

```sh
#!/bin/sh

JAIL_NAME="vito"
JAIL_IP_CIDR="192.168.128.13/17"
JAIL_GATEWAY="192.168.128.1"
JAIL_HOSTNAME="vito"
IFACE_NAME="igb0"
JAILS_PATH="/jails"
JAIL_ROOT="$JAILS_PATH/$JAIL_NAME"

# Create jail root
mkdir -p "$JAIL_ROOT"

# Install base system on jail root
bsdinstall jail "$JAIL_ROOT"

# Copy utility scripts
mkdir -p /usr/local/scripts/
install /usr/share/examples/jails/jib /usr/local/scripts/

# Jail definition
cat << EOF >> "/etc/jail.conf.d/$JAIL_NAME.conf"
pihole {
    vnet;
    vnet.interface="e0b_$JAIL_NAME";
    exec.prestart+="/usr/local/scripts/jib addm $JAIL_NAME $IFACE_NAME";
    exec.poststop+="/usr/local/scripts/jib destroy $JAIL_NAME";
    host.hostname = $JAIL_HOSTNAME;            # Hostname
    path = "$JAIL_ROOT";                       # Path to the jail
    mount.devfs;                               # Mount devfs inside the jail
    exec.start = "/bin/sh /etc/rc";            # Start command
    exec.stop = "/bin/sh /etc/rc.shutdown";    # Stop command
}
EOF

# Setup ip & default gateweay
cat << EOF >> "$JAIL_ROOT/etc/rc.conf"
ifconfig_e0b_$JAIL_NAME="$JAIL_IP_CIDR"
defaultrouter="$JAIL_GATEWAY"
EOF
```


## Linkdump

- https://github.com/exeba/FTL-freebsd-port/blob/main/examples/jail-setup.sh
- https://forum.opnsense.org/index.php?topic=26975.0
- https://www.reddit.com/r/opnsense/comments/sjewa4/jails_under_opnsense_221/?rdt=59758
- https://forum.opnsense.org/index.php?topic=26724.0
