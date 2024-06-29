<!-- StartUsingTheFwords, Version: 10, Modified: 2020/06/26, Author: feurig -->
# Start Using the F words.
Ubuntu's next long term support version 20.04 (Focal Fossa) is set to be released by the end of the month. In order to be prepared we should start using them. 

## Our experience so far
### Lxc container
I ran up a few new containers using our profiles and test for status around [ticket:42 recent issues with "resolve"d]. 

I am still working on whether or not this is resolved or if I broke it trying to get resolvd to listen to our servers using the init profiles.

The images are split into ubuntu/focal and ubuntu/focal/cloud. The cloud image picks up most of the profile changes and shows the most promise so far. This is a nice change given that most of the non-lts  images required tweaking before just working.
### upgraded containers
#### Ian / wordpress site
php7.2->7.4upgrade broke the site.

Removed mods-enabled/php7.2* 
	
	root@ian:/etc/apache2/mods-enabled# mv php7.2.* /tmp/
	
and enabled php7.4
	
	root@ian:/etc/apache2/mods-enabled# ln -s ../mods-available/php7.4* .
	
### susdev20 (changes to profile)
* update joe's passed and keys. (this does not replace ticket:44)  
* remove resolvd file creation
* add pihole update to update script. 

### Lxc server
I performed a do-release-upgrade -d on Joey.
	
	root@joey:~# do-release-upgrade -d -m server
	
It was flawless except that I had to run 
	
	#netplan apply
	
From the _console_ which pretty much fucks any chance of doing Bernie next. (At least until [ticket:36 the issues with console redirection are resolved]). 
#### BS2020
Once the console came back up I upgraded Bernie. ZFS pools needed to be updated after upgrade. Otherwise everything went pretty well.
### Notes

Major Changes.
* Lxd 4.0
* Php7.4
* Postgresql 12.

