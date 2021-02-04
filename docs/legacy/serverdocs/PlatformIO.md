I am looking to replace the Arduino framework with platform io and Xcode with Atom. The first test of this will be to program the [wiki:Esp8266] before moving back to the [wiki:Samd21 M0], [wiki:LeaflabsMaple Maple], and other [wiki: Arduino] boards.

Platformio is installed via pip.
	
	root@bob2:~# apt-get install python-pip
	... pip says we should upgrade ...
	root@bob2:~# pip install --upgrade pip
	...
	root@bob2:~# pip install platformio
	
once installed you can use it to get most of its dependencies. _(not sure I like the way it stores everything int its own space in my home directory)_
	
	don@bob2:~$ cd Documents
	don@bob2:~/Documents$ mkdir piotest
	don@bob2:~/Documents$ cd piotest
	don@bob2:~/Documents/piotest$ platformio init board=thingdev
	....
	save current ino file to directory and move it to src
	don@bob2:~/Documents/piotest$ mv mDNS_Web_Server/mDNS_Web_Server.ino src
	don@bob2:~/Documents/piotest$ platformio run --target upload
	...
	
	
	 
	
## Linkdump
* https://www.penninkhof.com/2015/12/1610-over-the-air-esp8266-programming-using-platformio/
* https://blog.openenergymonitor.org/2016/06/esp8266-ota-update/
* https://randomnerdtutorials.com/esp8266-ota-updates-with-arduino-ide-over-the-air/
* https://github.com/openenergymonitor/EmonESP
* https://blog.squix.org/2016/06/esp8266-continuous-delivery-pipeline-push-to-production.html
* https://www.thingforward.io/techblog/2016-11-22-getting-started-with-platformio-and-esp8266htmlmarkdown.html
* https://esp8266.github.io/Arduino/versions/2.0.0/doc/ota_updates/ota_updates.html
* https://www.bakke.online/index.php/2017/06/02/self-updating-ota-firmware-for-esp8266/
