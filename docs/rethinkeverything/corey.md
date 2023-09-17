# wordpress in 2023.
I still havn't managed to export my wordpress site into something static and maria free and I seem to need to keep using it even though the ui has become impossible to blog in. So I am readopting wordpress or at least trying to get it running on this years ubuntu and not hating it too much. Also upgrading the server from focal to jammy screws this site into something approaching disfunction usually only found at work work without the coresponding paycheck. 



OS ubuntu using apt install wordpress. 
WOOOT! We can install wordpress as a package!!!

```
apt update
apt install wordpress
apt install certbot python3-certbot-apache
cd /etc/apache2/sites-available/
```
Unfortunately its not that simple. The example from ubuntu sucks ass in terms of detail and the details are on the sites that hand roll the software. 

```
apt update
apt install wordpress
mysql
mysql -u root
apt install mysql-server
mysql -u root
apachectl start
cd /etc/wordpress/
ls
nano config-localhost.php
mysql -u www-data
mysql -u root
ls
nano /etc/apache2/sites-enabled/000-default.conf
apache2ctl restart
nano /etc/apache2/sites-enabled/000-default.conf
apache2ctl restart
ls /etc/apache2/mods-available/
a2enmod socach*
a2enmod ssl
systemctl restart apache2
ln -s config-localhost.php config-suspectdevices.com.php
apache2ctl restart
nano config-localhost.php
reboot
ip a
cd
ls .ssh/
ls .ssh/authorized_keys
cat .ssh/authorized_keys
cat ~joe/.ssh/authorized_keys >>.ssh/authorized_keys
cat ~feurig/.ssh/authorized_keys >>.ssh/authorized_keys
cat .ssh/authorized_keys
exit
cat /etc/apache2/sites-enabled/000-default.conf
chown -R www-data:www-data /usr/share/wordpress
nano /etc/wordpress/htaccess
nano /etc/wordpress/config-localhost.php
nano /usr/share/wordpress/wp-config.php
reboot
find / -name php.ini -print 2>/dev/null
nano /etc/php/8.1/apache2/php.ini
nano /etc/php/8.1/cli/php.ini
reboot
history
history|cut -c8-200
```

# the mother fucking issues.
1. Why the fuck do you move the location of the software when you package it.
2. Why the fuck dont you install mysql-server
3. Why the fuck does your default install not deal with the fact that NO ONE USES FTP FOR ANYTHING.
4. WHO THE FUCK BOTHERS TO EXPORT AND IMORT A SITE USING LESS THAN 2M of data.
5. Man the result of exporting a site and importing it creates some goddamned ugly site.
