<!-- LedeOpenWRT, Version: 1, Modified: 2018/12/02, Author: trac -->
# OpenWRT Notes

At a very minimum open the ssh port so that the router can be managed from the outside. Then disable logins (ssh keys only) in /etc/dropbear.
	
	root@OpenWrt:/etc/config# opkg update
	root@OpenWrt:/etc/config# opkg install nano
	
	root@OpenWrt:/etc/config# nano /etc/config/firewall
	
add the following
	
	
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.1'
	        option dest_port '22'
	        option name 'sshplease'
	        option src_dport '2222'
	
## allowing access to dell IDRAC 6 and server forward

## firewall setup on vpn
In order to get at the idrac and access BS2020 via ssh the following rules were added to /etc/config/firewall 
	
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.158'
	        option dest_port '22'
	        option name 'sshtobernie'
	        option src_dport '22'
	
	# idrac 6 redirections
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.121'
	        option dest_port '443'
	        option name 'idracplease1'
	        option src_dport '443'
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.121'
	        option dest_port '4433'
	        option name 'idracplease2'
	        option src_dport '4433'
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.121'
	        option dest_port '443'
	        option name 'idracplease3'
	        option src_dport '443'
	config redirect
	        option target 'DNAT'
	        option src 'wan'
	        option dest 'lan'
	        option proto 'tcp'
	        option dest_ip '192.168.1.121'
	        option dest_port '623'
	        option name 'idracplease4'
	        option src_dport '623'
	
Just to be paranoid we "#uci show" to make sure UCI picks up the rules then we "#uci commit" and reboot the router.

at this point we have full access to the servers idrac6
## Related Pages
### OpenVPN attempt #2
[wiki:OpenVPNOnLEDE OpenVPN on LEDE]
### Adventures in deploying OpenWRT/LEDE
* [wiki:OpenWRTonMR3020 Open WRT on TP-Link MR3020]
* [wiki:OpenWRTonLinkSysEA3500 Open WRT on LinkSYS EA3500]
