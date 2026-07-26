# Virgil Rebuild

## Standing up a new container

```sh
root@tk2022:~# incus profile edit admin-lan
config: {}
description: ""
devices:
  eth1:
    name: eth1
    nictype: bridged
    parent: br1
    type: nic
name: admin-lan
project: default
```

```sh
root@tk2022:~# incus init trixie -p default -p susdev25 -p admin-lan virgil -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  eth0:
    addresses:
      - 69.41.138.125/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
  eth1:
    addresses:
      - 192.168.31.228/24
EOF
)
"
```

### Fix resolv.conf

Now that we are debian based and are using the incus cloud images we should update our profile to set up resolv.conf correctly. In the mean time lets fix the foobarred install left by their cloud init. 

```
root@virgil:~# resolvconf -l
# resolv.conf from original.resolvconf
nameserver 69.41.138.98
nameserver 8.8.4.4
search suspectdevices.com fromhell.com vpn
# resolv.conf from systemd-resolved
nameserver 127.0.0.53
search suspectdevices.com fromhell.com vpn
root@virgil:~# systemctl stop systemd-resolved
root@virgil:~# systemctl disable systemd-resolved
root@virgil:~# rm /etc/resolv.conf
root@virgil:~# cat > /etc/resolv.conf <<EOD
> # resolv.conf from original.resolvconf
nameserver 69.41.138.98
nameserver 8.8.4.4
search suspectdevices.com fromhell.com vpn
> EOD
```

## Install tinyproxy

```sh
apt install tinyproxy -y
cat > /etc/tinyproxy/tinyproxy.conf <<EOD
User tinyproxy
Group tinyproxy
Port 3128
Listen 192.168.31.228
Timeout 600
DefaultErrorFile "/usr/share/tinyproxy/default.html"
StatFile "/usr/share/tinyproxy/stats.html"
LogLevel Info
PidFile "/run/tinyproxy/tinyproxy.pid"
MaxClients 10
Allow 192.168.31.1/24
ViaProxyName "tinyproxy"
EOD
systemctl enable --now tinyproxy
```

### Test tinyproxy

```sh
root@tk2022:~# curl -x 192.168.31.228:3128 http://archive.ubuntu.com/ubuntu/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /ubuntu</title>
```

## Wireguard

## References:

- https://oneuptime.com/blog/post/2026-03-02-how-to-disable-systemd-resolved-and-use-etc-resolv-conf-directly-on-ubuntu/view
- https://www.digithink.com/rethinkeverything/norouter/wireguard-and-tinyproxy/