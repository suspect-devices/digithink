```shell
08:21 <+stgraber> feurig: I believe I made a video about it an MAAS some time ago
08:21 <+stgraber> feurig: anyway, it's basically:
08:22 <+stgraber> lxc init my-pxe --empty --vm
08:22 <+stgraber> lxc config device override my-pxe eth0 boot.priority=10
08:22 <+stgraber> lxc start my-pxe --console=vga
08:22 <+stgraber> the boot.priority step is to have QEMU prefer network boot over local disk
08:23 <+stgraber> you may also want to grow the root disk depending on your needs: lxc config device override my-pxe root size=50GiB
```

# pure config is out of scope of this note
# setting up pure -> freebsd

# /etc/rc.conf.local
iscsid_enable="YES"
iscsictl_enable="YES"
iscsictl_flags="-Aa"
# grab rc.d file from zfs-backup2:/etc/rc.d/zpool_iscsi
# so system will try to import zpool after iscsi has settled
zpool_iscsi_enable="YES"


# /etc/iscsi.conf
pure01-ct0-1 {
        TargetAddress   = pure01-ct0-1.evergreen.laika.com
        SessionType     = Discovery
        InitiatorName   = iqn.2005-06.com.laika:freebsd-hostname.evergreen.laika.com
}
pure01-ct0-2 {
        TargetAddress   = pure01-ct0-2.evergreen.laika.com
        SessionType     = Discovery
        InitiatorName   = iqn.2005-06.com.laika:freebsd-hostname.evergreen.laika.com
}
pure01-ct1-1 {
        TargetAddress   = pure01-ct1-1.evergreen.laika.com
        SessionType     = Discovery
        InitiatorName   = iqn.2005-06.com.laika:freebsd-hostname.evergreen.laika.com
}
pure01-ct1-2 {
        TargetAddress   = pure01-ct1-2.evergreen.laika.com
        SessionType     = Discovery
        InitiatorName   = iqn.2005-06.com.laika:freebsd-hostname.evergreen.laika.com
}


service iscsid start
service iscsictl start

# view iscsi luns
iscsictl -L
# remove luns
iscsictl -Ra
# add luns
icsictl -Aa


# freebsd initiator doesn't handle multipath.
# The geom_multipath kernel module does 

# create multipath device
kldload geom_multipath
# make it survive a reboot
echo geom_multipath_load="YES" >> /boot/loader.conf
# 
gmultipath label mp0 da4 da5 da6 da7
# now you can create a zpool using the mp0 device
zpool create zjail multipath/mp0
zfs set mountpoint=/jails zjail
zpool set autotrim=on zroot
zfs set compression=off zjail
