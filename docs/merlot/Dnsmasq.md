
# DNSMasq 

dnsmasq is a caching dns and dhcp server that allows a single source of truth for
both. This replaces services such as bind and isc-dhcp. One of the nice things is
that once you give out an address to a host the host resolves to that address. 
The other nice thing is that it is file based

It was my hope that I could configure the dnsmasq provided by opnsense with files
that I could control but it insisted on requiring all settings be implimented via 
its gui and overwriting any manual files. So we are running dnsmasq on a separate 
server. 

At some point I will get this to work on a freebsd jail running on the router.


## sample dnsmasq.conf

```sh
#------------------------------------------------------------ dnsmasq.conf for figaro
# symlink as appropriate (linux=/etc/dnsmasq.conf,bsd=/usr/local/etc/dnsmasq.conf)
#
#
# Global stuff. 
#
#interface=igb0          # Only needed for freebsd
bind-interfaces          # Really bind only the configured interfaces
no-resolv                # Don't read /etc/resolv.conf for upstream DNS
no-poll
domain-needed
bogus-priv

#
# Logging
#

log-dhcp
log-queries
log-facility=/var/log/dnsmasq.log

#
# upstream dns
#
server=192.168.128.2
server=205.171.3.25
server=8.8.8.8
all-servers
cache-size=5000

#
# local dns configuration
#
auth-server=merlot,192.168.129.2
local=/merlot/
auth-zone=merlot,192.168.128.0/17
expand-hosts
#no-hosts

# 
# Dhcp configuration.
#
dhcp-ignore-clid
domain=merlot
dhcp-range=192.168.128.100,192.168.129.254
dhcp-option=option:router,192.168.128.1
#dhcp-option=option:ntp-server,192.168.0.4,10.10.0.5
#dhcp-host=D4:BE:D9:EC:EE:CE,192.168.31.49
#dhcp-option=vendor:PXEClient,1,192.168.31.2
dhcp-option=option:domain-search,merlot,merlot.suspectdevices.com,suspectdevices.com,digithink.com,fromhell.com,local
dhcp-option=option:dns-server,192.168.129.2,205.171.3.25,8.8.8.8
dhcp-authoritative
dhcp-hostsfile=/usr/local/merlot/dnsmasq/reservations.list

#
# cname 
#
conf-file=/usr/local/merlot/dnsmasq/cnames.list
```

## Generating the necessary files.


### one file to rule them all

We start with a csv file with all of the information we need.

```sh
domain,address,mac,name,notes,alias,,,
merlot,192.168.128.1,00:0e:b6:c0:1a:8b,misskitty,firewall,,,
...
```

### as little pile of python

```sh
#!/usr/bin/env python3
#------------------------------------------------------ creatednsmasqconfigs.py
# Given a csv file in the following format
# domain,address,mac,name,notes,alias,,,
#
# Generate the files used by dnsmasq (hosts,ether,reservations,cnames)
#
import sys
import csv

with open("/etc/hosts", "w") as h, \
     open("/etc/ethers", "w") as e, \
     open("/usr/local/merlot/dnsmasq/reservations.list", "w") as r, \
     open("/usr/local/merlot/dnsmasq/cnames.list", "w") as c:

    # should print comment header lines to each file here.
    print("127.0.0.1 localhost localhost.merlot localhost.merlot.suspectdevices.com",file=h)
    reader = csv.DictReader(open('/usr/local/merlot/data/merlot.csv'))
    for row in reader:
        if ('#' not in row['domain']): # skip commentted out lines (kassumes domain is first field)
            print(row['address']+' '+row['name']+' '+row['name']+'.'+row['domain'],file=h)
            print(row['mac']+' '+row['name']+'.'+row['domain'],file=e)
            print(row['mac']+','+row['address']+','+row['name']+',infinite',file=r)
            if (row['alias']):
                print('cname='+row['alias']+','+row['alias']+'.'+row['domain']+\
                    ','+row['name']+'.'+row['domain'],file=c)

```

### files generated 

* /etc/hosts
```sh
127.0.0.1 localhost localhost.merlot localhost.merlot.suspectdevices.com
192.168.128.1 misskitty misskitty.merlot
```
* /etc/hosts
```sh 
00:0e:b6:c0:1a:8b misskitty.merlot
```
* reservations
```sh
00:0e:b6:c0:1a:8b,192.168.128.1,misskitty,infinite
```
* cnames
```sh
cname=firewall,firewall.merlot,misskitty.merlot
```

## references

* https://oneuptime.com/blog/post/2026-01-15-setup-dnsmasq-local-dns-ubuntu/view



