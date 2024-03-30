# Wordpress in 2024
After 3+ years of trying, I still havn't managed to export my wordpress site into something static and maria free and I seem to need to keep using it even though the ui has become impossible to blog in. So I am readopting wordpress or at least trying to get it running on this years ubuntu and not hating it too much. Also upgrading the existing server from focal to jammy screws this site into something approaching disfunction usually only found at work work without the coresponding paycheck.

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

# the mother obscening issues (based on 2023s attempt)
1. Why the obscenity do you move the location of the software when you package it.
2. Why the obscenity don't you install mysql-server
3. Why the obscenity does your default install not deal with the fact that NO ONE USES FTP FOR ANYTHING.
4. WHO THE OBSCENITY BOTHERS TO EXPORT AND IMPORT A SITE USING LESS THAN 2M of data.
5. Man the result of exporting a site and importing it creates some goddamned ugly site.

## References

- https://www.hostinger.com/tutorials/fix-the-uploaded-file-exceeds-the-upload-max-filesize-directive-in-php-ini-wordpress
- https://stackoverflow.com/questions/37157264/wordpress-plugin-install-could-not-create-directory
- THIS https://www.linode.com/docs/guides/how-to-install-wordpress-ubuntu-22-04/
-https://ubuntu.com/server/docs/how-to-install-and-configure-wordpress

### THIS
(Optional) WordPress typically uses FTP credentials to install new themes and plug-ins. Add the following lines to the wp_config.php file to remove this restriction. This file is located in the root directory for the domain inside the public_html subdirectory.

File: /var/www/html/example.com/public_html/wp-config.php
```
/** Bypass FTP */
define('FS_METHOD', 'direct');
```