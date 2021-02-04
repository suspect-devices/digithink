Nigel is a TP-Link Mr3020 router running LEDE 17.01.3 that I am using to connect things to the net. Things are connected in one of 2 ways.

* wifi
* serial
* usb-serial
* 3.3V serial.

## Wifi 
Nigel provides a Hidden wifi access point called critters on the internal lan (192.168.2.0/24)
	
	root@nigel:~# nano /etc/config/wireless 
	config wifi-device  radio0
		option type     mac80211
		option channel  11
		option hwmode	11g
		option path	'platform/ar933x_wmac'
		option htmode	HT20
		option disabled 0
	
	config wifi-iface
		option device   radio0
		option network  lan
		option hidden	1
		option mode     ap
		option ssid     cr1tt3rs
		option encryption psk2
	        option key      '********'
	root@nigel:~# 
	

* [wiki:OpenWRTonMR3020 Setting up OpenWRT (15.05) on a TP-link MR3020]
* https://downloads.lede-project.org/releases/17.01.4/targets/ar71xx/generic/