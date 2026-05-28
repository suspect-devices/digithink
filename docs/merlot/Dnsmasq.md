
# DNSMasq 

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

```sh
domain,address,mac,name,notes,alias,,,
merlot,192.168.128.1,00:0e:b6:c0:1a:8b,misskitty,firewall,,,

```

```sh
#!/usr/bin/env python3
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
        print(row['address']+' '+row['name']+' '+row['name']+'.'+row['domain'],file=h)
        print(row['mac']+' '+row['name']+'.'+row['domain'],file=e)
        print(row['mac']+','+row['address']+','+row['name']+',infinite',file=r)
        if (row['alias']):
            print('cname='+row['alias']+','+row['alias']+'.'+row['domain']+\
                  ','+row['name']+'.'+row['domain'],file=c)

```

## references

* https://oneuptime.com/blog/post/2026-01-15-setup-dnsmasq-local-dns-ubuntu/view



