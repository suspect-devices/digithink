# Replacing the colo router with a container.

After working through the complexities of using headscale/tailscale I realized that I really only needed the colo router to do 2 things.

1. Provide us access to the admin lan (the servers and their remote consoles).

    ```mermaid
    graph LR
    D([192.168.31.0/24])<-->A[Host interface]
    D<-->E[Host Drac/ILO]
    C[laptop] <-- Wireguard --> B(homer/virgil);
    B <-- Wireguard -->D;
    ```

2. Allow the servers to reach the update repositories.

    ```mermaid
    graph LR
    B --> I([internet])
    A[Host] -- Apt Via Proxy --> B(homer/virgil);
    ```

By using a container with access to both the external lan and the admin lan we can set up wireguard and tinyproxy. Wireguard allows us to securely connect to the admin lan while tinyproxy allows the servers a mechanism to recieve software updates. This will become a staging/test setup for [the colo firewall](https://www.digithink.com/rethinkeverything/norouter/using-a-tank-for-crowd-control/).

## SETTING UP THE CONTAINER
To be able to do its job the container needed to be privilaged and it also would not run on 22.04. Its ok 22.04 still has a few years of support left.
```sh
root@aoc2024:~# lxc init ubuntu:22.04 homer -c security.privileged=true -p susdev23 -p infra
root@aoc2024:~# lxc config edit homer
name: homer
description: "wireguard/squid host"
...
devices:
  eth1:
    name: eth1
    nictype: bridged
    parent: br3
    type: nic
^x
root@aoc2024:~# lxc start homer
root@aoc2024:~# lxc exec homer bash
root@homer:~# nano /etc/netplan/50-cloud-init.yaml
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 198.202.31.227/25
            nameservers:
                addresses:
                - 198.202.31.132
                - 8.8.8.8
                search:
                - suspectdevices.com
                - styx.suspectdevices.com
            routes:
            -   to: default
                via: 198.202.31.129
        eth1:
            addresses:
            - 192.168.31.227/24
^x
root@homer:~# netplan apply
```

Backcheck the interfaces

```sh
root@homer:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
45: eth0@if46: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:ba:f0:be brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 198.202.31.227/25 brd 198.202.31.255 scope global eth0
       valid_lft forever preferred_lft forever
47: eth1@if48: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:2e:6f:d8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.31.227/24 brd 192.168.31.255 scope global eth1
       valid_lft forever preferred_lft forever
```

### Install prerequisites and enable ip forwarding

The next few sections are done on the gateway container (homer)

```sh
apt install wireguard
apt install resolvconf
sysctl -w net.ipv4.ip_forward=1
```

### Clone it
Once you have a working system clone it to the other server and adjust its configuration as needed.
```sh
lxc snapshot aoc2024:homer 19jun24
lxc copy aoc2024:homer/19jun24 virgil
lxc config edit virgil
```

## Wireguard

### Set up wireguard 

#### Server Setup

```sh
cd /etc/wireguard/
wg genkey | sudo tee private.key
chmod go= private.key
cat private.key | wg pubkey | sudo tee public.key
wg genpsk |tee preshared.psk
nano /etc/wireguard/wg0.conf
```

```ini
# wg0.conf
[Interface]
Address = 10.0.0.1/32
ListenPort = 1194
PrivateKey = <<contents of private.key>>
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE

# merlot
[Peer]
PublicKey = <<contents of public.key>>
AllowedIPs =  10.0.0.2/32,192.168.128.0/17
PresharedKey = <<contents of preshared.key>>

# amyl dons laptop
[Peer]
PublicKey = <<key from wireguard client>>
AllowedIPs = 10.0.0.3/32
PresharedKey = <<contents of preshared.key>>
```
##### Enable it

```sh
wg-quick up wg0
systemctl enable wg-quick@wg0
```

#### Client Configuration.

YOU ARE HERE Describing client configuration.
##### MacOs client
##### Linux client

## No ~~Squid~~ 

The last update to squid completely overwrote its working configuration file without even making a backup copy. Can you say exposure and disfunction?
FRACK THAT. IT'S GONE.

```sh
root@virgil:/etc/squid# apt remove --purge squid
```

## TinyProxy -- proxy for main servers

### Setting up TinyProxy

This is on virgil (x.x.x.228) repeat this on sitka (x.x.x.2)

```sh
apt install tinyproxy -y
systemctl enable tinyproxy
cd /etc/tinyproxy/
cp tinyproxy.conf tinyproxy.conf.noisy
grep -v "^\#" tinyproxy.conf.noisy |grep -v "^$" >tinyproxy.conf
nano tinyproxy.conf
```

```sh
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
```

```sh
systemctl enable tinyproxy
systemctl start tinyproxy
```

### Test the proxy

```sh
root@kb2018:~# curl -x 192.168.31.228:3128 http://archive.ubuntu.com/ubuntu
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="http://archive.ubuntu.com/ubuntu/">here</a>.</p>
<hr>
<address>Apache/2.4.52 (Ubuntu) Server at archive.ubuntu.com Port 80</address>
</body></html>
```

### Set up apt to use proxy

```sh
nano /etc/apt/apt.conf.d/80proxy.conf
```

```sh
Acquire::http::Proxy "http://192.168.31.227:3128/";
```

### Test apt through proxy

```sh
root@aoc2024:/etc/apt/apt.conf.d# ip route delete default
root@aoc2024:/etc/apt/apt.conf.d# ip route
192.168.31.0/24 dev br3 proto kernel scope link src 192.168.31.158
root@aoc2024:/etc/apt/apt.conf.d# apt update
Hit:1 http://us.archive.ubuntu.com/ubuntu noble InRelease
Get:2 https://pkgs.tailscale.com/stable/ubuntu noble InRelease
Hit:3 http://us.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:5 http://us.archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 6575 B in 1s (9357 B/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date.
```

## References / Linkdump

- <https://www.wireguard.com>
- <https://www.freecodecamp.org/news/build-your-own-wireguard-vpn-in-five-minutes/>
- <https://linuxiac.com/how-to-use-apt-with-proxy/>
- <https://askubuntu.com/questions/257290/configure-proxy-for-apt#257296>
- <https://tinyproxy.github.io>

