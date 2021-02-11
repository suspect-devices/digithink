#OpenVPN on LEDE (Fail)
Now that we have a recent version of the operating system OpenVPN seems to work as advertised. Following the instructions at https://lede-project.org/docs/user-guide/openvpn.server. Much of the heavy lifting is done by easyRSA and MakeOpenVPN.sh. 

The client setups fail if you use an empty passphrase which is good. OTOH In my initial attempts I could not get the server certificates to work with one. When in doubt read the documentation sections on the old openWRT site. It provides a little more depth but there still are some missing pieces that  require more exploration (https://wiki.openwrt.org/doc/howto/vpn.openvpn#tab__using_openssl_commands_most_secure). 

For the client I used tunnelblick which works well and takes the .ovpn configuration files created by this process.
### Sample Install
* follow the bouncing prompt using lede user guide.
	
	root@mullein:~# opkg update && opkg install openvpn-openssl openvpn-easy-rsa luci-app-openvpn
	Downloading ..... 
	.....note additional dependencies.....
	Configuring kmod-tun.
	Configuring zlib.
	Configuring libopenssl.
	Configuring openssl-util.
	Configuring liblzo.
	Configuring openvpn-openssl.
	Configuring openvpn-easy-rsa.
	Configuring luci-app-openvpn.
	root@mullein:~# cd /etc/easy-rsa
	root@mullein:/etc/easy-rsa# source vars
	NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/easy-rsa/keys
	root@mullein:/etc/easy-rsa# clean-all
	NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/easy-rsa/keys
	root@mullein:/etc/easy-rsa# build-ca
	NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/easy-rsa/keys
	Generating a 2048 bit RSA private key
	..................+++
	............................................................................+++
	writing new private key to 'ca.key'
	-----
	You are about to be asked to enter information that will be incorporated
	into your certificate request.
	What you are about to enter is what is called a Distinguished Name or a DN.
	There are quite a few fields but you can leave some blank
	For some fields there will be a default value,
	If you enter '.', the field will be left blank.
	-----
	Country Name (2 letter code) [US]:
	State or Province Name (full name) [CA]:OR
	Locality Name (eg, city) [SanFrancisco]:Portland
	Organization Name (eg, company) [Fort-Funston]:SuspectDevices
	Organizational Unit Name (eg, section) [MyOrganizationalUnit]:3dAngst
	Common Name (eg, your name or your server's hostname) [Fort-Funston CA]:mullein
	Name [EasyRSA]:mullein
	Email Address [me@myhost.mydomain]:don@suspectdevices.com
	
* plan on the next step taking so long you will probably have to reconnect and pick up where you were...
	
	root@mullein:/etc/easy-rsa# build-dh
	NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/easy-rsa/keys
	Generating DH parameters, 2048 bit long safe prime, generator 2
	This is going to take a long time
	.... 
	.... They are not kidding ....
	.........................................................................+.....++*++*
	
* continue to follow the bouncing prompt
	
	root@mullein:/etc/easy-rsa# build-key-server mullein
	..... answer the questions ....
	A challenge password []:
	An optional company name []:
	Using configuration from /etc/easy-rsa/openssl-1.0.0.cnf
	Check that the request matches the signature
	Signature ok
	The Subject's Distinguished Name is as follows
	countryName           :PRINTABLE:'US'
	stateOrProvinceName   :PRINTABLE:'OR'
	localityName          :PRINTABLE:'Portland'
	organizationName      :PRINTABLE:'SuspectDevices'
	organizationalUnitName:PRINTABLE:'3dAngst'
	commonName            :PRINTABLE:'mullein'
	name                  :PRINTABLE:'mullein'
	emailAddress          :IA5STRING:'don@suspectdevices.com'
	Certificate is to be certified until Oct 23 23:46:35 2027 GMT (3650 days)
	Sign the certificate? [y/n]:y
	1 out of 1 certificate requests certified, commit? [y/n]y
	Write out database with 1 new entries
	Data Base Updated
	root@mullein:/etc/easy-rsa# openvpn --genkey --secret /etc/easy-rsa/keys/ta.key
	
* set up the network and firewall rules.
	
	root@mullein:/etc/easy-rsa# openvpn --genkey --secret /etc/easy-rsa/keys/ta.key
	root@mullein:/etc/easy-rsa# uci set network.vpn0="interface"
	root@mullein:/etc/easy-rsa# uci set network.vpn0.ifname="tun0"
	root@mullein:/etc/easy-rsa# uci set network.vpn0.proto="none"
	root@mullein:/etc/easy-rsa# uci set network.vpn0.auto="1"
	root@mullein:/etc/easy-rsa# uci commit network
	root@mullein:/etc/easy-rsa# uci add firewall rule
	cfg1892bd
	root@mullein:/etc/easy-rsa# uci set firewall.@rule[-1].name="Allow-OpenVPN-Inbound"
	root@mullein:/etc/easy-rsa# uci set firewall.@rule[-1].target="ACCEPT"
	root@mullein:/etc/easy-rsa# uci set firewall.@rule[-1].src="wan"
	root@mullein:/etc/easy-rsa# uci set firewall.@rule[-1].proto="udp"
	root@mullein:/etc/easy-rsa# uci set firewall.@rule[-1].dest_port="1194"
	root@mullein:/etc/easy-rsa# uci add firewall zone
	cfg19dc81
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].name="vpn"
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].input="ACCEPT"
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].forward="ACCEPT"
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].output="ACCEPT"
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].masq="1"
	root@mullein:/etc/easy-rsa# uci set firewall.@zone[-1].network="vpn0"
	root@mullein:/etc/easy-rsa# uci add firewall forwarding
	cfg1aad58
	root@mullein:/etc/easy-rsa# uci set firewall.@forwarding[-1].src="vpn"
	root@mullein:/etc/easy-rsa# uci set firewall.@forwarding[-1].dest="wan"
	root@mullein:/etc/easy-rsa# uci add firewall forwarding
	cfg1bad58
	root@mullein:/etc/easy-rsa# uci set firewall.@forwarding[-1].src="vpn"
	root@mullein:/etc/easy-rsa# uci set firewall.@forwarding[-1].dest="lan"
	root@mullein:/etc/easy-rsa# uci commit firewall
	root@mullein:/etc/easy-rsa# /etc/init.d/network reload
	....
	root@mullein:/etc/easy-rsa# /etc/init.d/firewall reload
	....
	
* check ip forwarding
	
	root@mullein:/etc/easy-rsa# cat /proc/sys/net/ipv4/ip_forward
	1
	
* edit /etc/config/openvpn, enable and restart daemon.
	
	root@mullein:/etc/easy-rsa# nano /etc/config/openvpn
	... add the following (change name, cert, and key to match your server) ...
	##########################################################
	# https://lede-project.org/docs/user-guide/openvpn.server
	##########################################################
	config openvpn 'mullein'
		option enabled '1'
		option dev 'tun'
		option port '1194'
		option proto 'udp'
		option status '/var/log/openvpn_status.log'
		option log '/tmp/openvpn.log'
		option verb '3'
		option mute '5'
		option keepalive '10 120'
		option persist_key '1'
		option persist_tun '1'
		option user 'nobody'
		option group 'nogroup'
		option ca '/etc/easy-rsa/keys/ca.crt'
		option cert '/etc/easy-rsa/keys/mullein.crt'
		option key '/etc/easy-rsa/keys/mullein.key'
		option dh '/etc/easy-rsa/keys/dh2048.pem'
		option mode 'server'
		option tls_server '1'
		option tls_auth '/etc/easy-rsa/keys/ta.key 0'
		option server '10.9.0.0 255.255.255.0'
		option topology 'subnet'
		option route_gateway 'dhcp'
		option client_to_client '1'
		list push 'persist-key'
		list push 'persist-tun'
		list push 'redirect-gateway def1'
		# allow your clients to access to your network
		list push 'route 192.168.2.0 255.255.255.0'
		# push DNS to your clients
		list push 'dhcp-option DNS 192.168.2.1'
		option comp_lzo 'no'
	
	
	root@mullein:/etc/easy-rsa# /etc/init.d/openvpn start
	root@mullein:/etc/easy-rsa# /etc/init.d/openvpn enable
	root@mullein:/etc/easy-rsa# cat  /tmp/openvpn.log
	...
	Thu Oct 26 00:22:46 2017 OpenVPN 2.4.3 mipsel-openwrt-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [MH/PKTINFO] [AEAD]
	....
	Thu Oct 26 00:22:46 2017 MULTI: multi_init called, r=256 v=256
	Thu Oct 26 00:22:46 2017 IFCONFIG POOL: base=10.9.0.2 size=252, ipv6=0
	Thu Oct 26 00:22:46 2017 Initialization Sequence Completed
	...
	
* create client cert.
	
	root@mullein:~# cd /etc/easy-rsa/
	root@mullein:/etc/easy-rsa# source vars
	NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/easy-rsa/keys
	root@mullein:/etc/easy-rsa# build-key-pkcs12 donathome
	...
	writing new private key to 'donathome.key'
	....
	Country Name (2 letter code) [US]:
	State or Province Name (full name) [CA]:OR
	Locality Name (eg, city) [SanFrancisco]:Portland
	Organization Name (eg, company) [Fort-Funston]:SuspectDevices
	Organizational Unit Name (eg, section) [MyOrganizationalUnit]:3dAngst
	Common Name (eg, your name or your server's hostname) [donathome]:viscious
	Name [EasyRSA]:DonAtHome
	Email Address [me@myhost.mydomain]:don@suspectdevices.com
	
	Please enter the following 'extra' attributes
	to be sent with your certificate request
	A challenge password []:XXXXXXXXXXXX
	An optional company name []:Its Late
	...
	Certificate is to be certified until Oct 24 02:49:46 2027 GMT (3650 days)
	Sign the certificate? [y/n]:y
	
	
	1 out of 1 certificate requests certified, commit? [y/n]y
	Write out database with 1 new entries
	Data Base Updated
	Enter Export Password:
	Verifying - Enter Export Password:
	root@mullein:/etc/easy-rsa# openssl rsa -in /etc/easy-rsa/keys/donathome.key -des3 -out /etc/easy-rsa/keys/donathome.3des.key
	writing RSA key
	Enter PEM pass phrase:
	Verifying - Enter PEM pass phrase:
	root@mullein:/etc/easy-rsa# 
	
* MakeOpenVPN.sh script (install missing dependencies)
	
	root@mullein:/etc/easy-rsa# cd keys
	root@mullein:/etc/easy-rsa/keys# wget https://gist.githubusercontent.com/ivanmarban/57561e2bacf3b3a709426d353d2b6584/raw/30bf3c86fbc95a0a
	5d53d0aac348bcebdc9aa2eb/MakeOpenVPN.sh -O /etc/easy-rsa/keys/MakeOpenVPN.sh
	wget: SSL support not available, please install one of the libustream-ssl-* libraries as well as the ca-bundle and ca-certificates packages.
	root@mullein:/etc/easy-rsa/keys# opkg update && opkg install libustream-openssl ca-certificates 
	...
	root@mullein:/etc/easy-rsa/keys# wget https://gist.githubusercontent.com/ivanmarban/57561e2bacf3b3a709426d353d2b6584/raw/30bf3c86fbc95a0a
	5d53d0aac348bcebdc9aa2eb/MakeOpenVPN.sh -O /etc/easy-rsa/keys/MakeOpenVPN.sh
	Downloading 'https://gist.githubusercontent.com/ivanmarban/57561e2bacf3b3a709426d353d2b6584/raw/30bf3c86fbc95a0a5d53d0aac348bcebdc9aa2eb/MakeOpenVPN.sh'
	Connecting to 151.101.52.133:443
	Writing to '/etc/easy-rsa/keys/MakeOpenVPN.sh'
	/etc/easy-rsa/keys/M 100% |*******************************|  1839   0:00:00 ETA
	Download completed (1839 bytes)
	root@mullein:/etc/easy-rsa/keys# chmod oug+x MakeOpenVPN.sh 
	
* configure and run script.
	
	root@mullein:/etc/easy-rsa/keys# nano Default.txt
	... Add the following, Adjust host name accordingly ....
	client
	dev tun
	proto udp
	remote mullein.suspectdevices.com 1194
	resolv-retry infinite
	nobind
	mute-replay-warnings
	ns-cert-type server
	key-direction 1
	verb 1
	mute 20
	comp-lzo no
	root@mullein:/etc/easy-rsa/keys# ./MakeOpenVPN.sh 
	Please enter an existing Client Name:
	donathome
	Client's cert found: donathome
	Client's Private Key found: donathome.3des.key
	CA public Key found: ca.crt
	tls-auth Private Key found: ta.key
	Done! donathome.ovpn Successfully Created.
	root@mullein:/etc/easy-rsa/keys# ls
	01.pem              ca.crt              donathome.key       index.txt.old       mullein.key         myvpn.key
	02.pem              ca.key              donathome.ovpn      knight.crt          mullien.crt         serial
	03.pem              dh2048.pem          donathome.p12       knight.csr          mullien.csr         serial.old
	04.pem              donathome.3des.key  index.txt           knight.key          mullien.key         ta.key
	Default.txt         donathome.crt       index.txt.attr      mullein.crt         myvpn.crt
	MakeOpenVPN.sh      donathome.csr       index.txt.attr.old  mullein.csr         myvpn.csr
	root@mullein:/etc/easy-rsa/keys# ./MakeOpenVPN.sh 
	Please enter an existing Client Name:
	donathome
	Client's cert found: donathome
	Client's Private Key found: donathome.3des.key
	CA public Key found: ca.crt
	tls-auth Private Key found: ta.key
	Done! donathome.ovpn Successfully Created.
	
### References (Link Dump)
* https://help.my-private-network.co.uk/support/solutions/articles/24000005597-openwrt-lede-openvpn-setup
* https://lede-project.org/docs/user-guide/openvpn.server#setup_clients
* https://steemit.com/openwrt/@rbrthnk/vpn-pptp-router-with-openwrt-lede-tutorial-super-easy
* https://lede-project.org/docs/user-guide/tunneling_interface_protocols
* https://www.softether.org/4-docs/2-howto/9.L2TPIPsec_Setup_Guide_for_SoftEther_VPN_Server
* https://wiki.gentoo.org/wiki/IPsec_L2TP_VPN_server
* http://connect.rbhs.rutgers.edu/vpn/Mac_OSX_Native_VPN_Client_Overview.pdf
* http://cookbook.fortinet.com/ipsec-vpn-native-mac-os-client-54/
* https://www.howtogeek.com/216209/how-to-connect-your-mac-to-any-vpn-and-automatically-reconnect/
* https://tunnelblick.net/cInstall.html
* https://forum.lede-project.org/t/configuring-lede-router-with-a-pppoe-modem-router/5348/2
* https://wiki.openwrt.org/doc/howto/openconnect-setup
* https://wiki.gavowen.ninja/doku.php?id=lede:openconnect#tab__pki_templates
* https://lede-project.org/docs/user-guide/openvpn.server
* https://wiki.openwrt.org/doc/howto/vpn.openvpn#tab__traditional_tun_client