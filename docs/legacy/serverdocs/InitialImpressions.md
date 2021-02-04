# You may say to yourself "Well, How did I get here?"
_(first attempts at setting things up)_

This is my collection of notes on how the servers we own and operate were set up. 

## medea, BS2020 and other hardware in the ONB building
[ Google Doc with map of bresgal/suspect devices IP Addresses](https://docs.google.com/spreadsheets/d/1KRkqdYvgRtV4vu6AGzdLWJVGTIsV2o2iSSJBEFMZJAw/edit#gid=0)

### BS2020, (KB2020) Virtualization server(s)
#### BS2020
BS2020 is an upgrade for bernie with an eye on modern hardware and virtualization. The hardware is a Dell R610 from Server Monkey with 12 processors and 96 Gig of memory. 

[wiki:BS2020InstallNotes BS2020 Install Notes]

#### KB2020
The addition of a second server is planned using similar hardware. 

### LXC

[wiki:LXDContainersWithProfile Creating Lxd Containers with static ip and admin users]



#### Docker Host


[wiki:DockerInstallNotes Initial Docker Install on franklin]

#### Virtualized Medea

For years now Medea (a pile of junk that Joe found) has been providing DNS, Websites and Email to all of our domains. (including this site until recently) These services have been migrated to LXC containers and moved to BS2020.

[wiki:MigratingServicesToLXC Server Migration -- Theory and practice]


#### Admin Network (Currently the dot 1)

In order to provide better security for virtual hosts (and to even consider a secure openstack) a separate network for the administrative lan is required. There are several ways that we could achieve this including the vpn connection that Sudti offered to provide, as well as purchasing a dedicated vpn capable firewall. 

In a perfect world we should be able to use openVPN to securely connect to the admin network since both openstack and the idrac use several ports to provide GUI and web interfaces and neither can be securely exposed to the internet. 

The availability of cheap wifi routers capable or running openwrt or dd-wrt makes it possible to configure and deploy our own vpn tailored to our needs. When we started this process openWRT had still not merged with LEDE (and it still hasn't but all active development is on the LEDE side including a workable openVPN implementation). We have an openWRT (15.04) router in place which has a set of workaround firewall rules to allow us access to bs2020,

 We have provisioned an LEDE router (knight) with a working VPN and are waiting for a MOP to swap it out.



=#### OpenWRT=
[wiki:OpenWRT OpenWRT Setup]

=#### Remote Control (Dell IDRAC)=

## Other stuff on the site
* [wiki:7900NWashburne Home Network adventures]
* [wiki:Feurig feurigs todo list.]
* [wiki:Trac109Blurb old start page]

## References
* https://docs.openstack.org/devstack/latest/guides/lxc.html
* https://stackoverflow.com/questions/15658932/completely-remove-openstack-from-system-after-installation-from-devstack-script
* https://help.ubuntu.com/lts/serverguide/lxc.html
* https://stackoverflow.com/questions/24824325/is-there-a-way-to-use-dnsmasq-and-bind-on-the-same-computer
* http://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/setup-linux-container-with-lxc-on-ubuntu-16-04-14-04.html
* https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04