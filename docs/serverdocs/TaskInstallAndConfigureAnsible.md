<!-- TaskInstallAndConfigureAnsible, Version: 9, Modified: 2019/02/26, Author: feurig -->
# Install Ansible
All centralized maintanance should be initiated from kb2018
	
	root@kb2018:~# apt-get install ansible
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following additional packages will be installed:
	  ieee-data python-asn1crypto python-certifi python-cffi-backend python-chardet python-cryptography python-enum34 python-httplib2 python-idna python-ipaddress
	  python-jinja2 python-jmespath python-kerberos python-libcloud python-lockfile python-markupsafe python-netaddr python-openssl python-paramiko python-pkg-resources
	  python-pyasn1 python-requests python-selinux python-simplejson python-six python-urllib3 python-xmltodict python-yaml
	Suggested packages:
	  cowsay sshpass python-cryptography-doc python-cryptography-vectors python-enum34-doc python-jinja2-doc python-lockfile-doc ipython python-netaddr-docs
	  python-openssl-doc python-openssl-dbg python-gssapi python-setuptools python-socks python-ntlm
	...
	root@kb2018:~# 
	
## Install python to all containers
	
	root@kb2018:~# for h in `lxc list local: -c n --format csv ` ;do echo $h;lxc exec local:$h  -- apt-get install -y python; done
	...
	root@kb2018:~# for h in `lxc list bs2020: -c n --format csv ` ;do echo $h;lxc exec bs2020:$h  -- apt-get install -y python; done
	...
	
## Seed /etc/ansible/hosts
### localhost (kb2018)

  Adding the entry for the localhost is simple
	
	root@kb2018:~#  nano /etc/ansible/hosts 
	
	[pets:children]
	servers
	containers
	
	[servers]
	kb2018   ansible_connection=local
	..
	root@kb2018:~# 
	
### local containers

  entries  for local containers is equally straightforward.
	
	hostname ansible_connection=lxd
	
  Which we can generate using lxc list and awk
	 
	root@kb2018:~# lxc list -c n --format=csv local:|awk '{print $1,"ansible_connection=lxd";}'>>/etc/ansible/hosts
	

### containers on remote host

 Containers on the remote host (bs2020) require an additional parameter
 	
	 remotecontainer  ansible_connection=lxd ansible_host=remotehost:remotecontainer
	
 Which we again generate using lxc list and awk
	
	root@kb2018:~# lxc list -c n --format=csv bs2020:|awk '{print $1," ansible_connection=lxd ansible_host=bs2020:"$1;}'>>/etc/ansible/hosts
	

##adding access to bs2020 (via ssh to unprivileged account)
Our current security model expressly forbids direct access to all root accounts, users must connect using an ssh key and escalate using their password. 

To control a remote server from ansible user (root@kb2018) we:

Create a sudo user for our ansible host
	
	root@bs2020:~# useradd kb2018 -c"Governer Kate Brown" -m -g sudo
	root@bs2020:~# passwd kb2018
	... remember this one for later ...
	
Restrict ssh access to that account to the ip of that particular host.
	
	root@bs2020:~# nano /etc/ssh/sshd_config 
	...
	PermitRootLogin no
	....
	DenyUsers kb2018@"!192.168.31.159,*"
	...
	root@bs2020:~# service ssh restart
	
	
Generate key for our ansible user (root@kb2018)
	
	haifisch:~ don$ ssh -p22222 feurig@bs2020.suspectdevices.com
	...
	Last login: Mon Feb 25 18:56:59 2019 from 97.115.103.251
	feurig@kb2018:~$ sudo bash
	[sudo] password for feurig: 
	root@kb2018:~# ssh-key
	ssh-keygen   ssh-keyscan  
	root@kb2018:~# ssh-keygen 
	Generating public/private rsa key pair.
	Enter file in which to save the key (/root/.ssh/id_rsa): 
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /root/.ssh/id_rsa.
	Your public key has been saved in /root/.ssh/id_rsa.pub.
	The key fingerprint is:
	... 
	... add ssh key to kb2018@bs2020:.ssh/authorized_keys ...
	...
	
	root@kb2018:~# ssh kb2018@bs2020.suspectdevices.com
	

## Testing connectivity.
At this point we can add the remote server to ansible's inventory and check the connectivity.
	
	bs2020   ansible_connection=ssh ansible_ssh_user=kb2018 
	 
_note kb2018 is the localhost, ernest24jan19 (stopped) and douglas are local containers, bs2020 is a remote host and teddy is a container that it hosts_
	
	root@kb2018:~# ansible pets -m ping
	kb2018 | SUCCESS => {
	    "changed": false, 
	    "ping": "pong"
	}
	ernest24jan19 | UNREACHABLE! => {
	    "changed": false, 
	    "msg": "... , exited with result 1", 
	    "unreachable": true
	}
	...
	douglas | SUCCESS => {                                                                                                                                           
	    "changed": false, 
	    "ping": "pong"
	}
	...
	bs2020 | SUCCESS => {
	    "changed": false, 
	    "ping": "pong"
	}
	...
	teddy | SUCCESS => {
	    "changed": false, 
	    "ping": "pong"
	}
	root@kb2018:~# 
	
However we cannot run privileged commands on our remote host.
	
	root@kb2018:~# ansible servers -m apt -a "force_apt_get=yes upgrade=yes update_cache=yes autoremove=yes"
	bs2020 | FAILED! => {
	    "changed": false, 
	    "msg": "Failed to lock apt for exclusive operation"
	}
	kb2018 | SUCCESS => {
	
We can fix this by telling ansible to escalate using our user and password
	
	bs2020   ansible_host=bs2020.suspectdevices.com ansible_user=kb2018ansible_become=yes ansible_become_user=root ansible_become_pass=my_super_secret_password
	
And we can see that this works. 
Next we encrypt the password using ansible's vault feature and moving the username and password to the host_vars file.

	
	feurig@kb2018:~$ grep 'bs2020 ' /etc/ansible/hosts
	bs2020   ansible_host=bs2020.suspectdevices.com ansible_user='{{ bs2020_unprivilaged_user }}' ansible_become=yes ansible_become_user=root ansible_become_pass='{{ bs2020_become_pass }}'
	root@kb2018:~# ansible servers -m apt -a "force_apt_get=yes upgrade=yes update_cache=yes autoremove=yes" 
	kb2018 | SUCCESS => {
	

_... WIP: you are here ..._
Create and protect vault password file
	
	root@kb2018:~# openssl rand -base64 2048 >  /root/.vault_passwd
	root@kb2018:~# chmod 600 /root/.vault_passwd 
	
Add password file to ansible.cfg
	
	root@kb2018:~# nano /etc/ansible/ansible.cfg
	...
	# If set, configures the path to the Vault password file as an alternative to
	# specifying --vault-password-file on the command line.
	#vault_password_file = /path/to/vault_password_file
	vault_password_file=/root/.vault_passwd
	...
	
Encrypt sudo password 
	
	root@kb2018:~# ansible-vault encrypt_string 'mybigsecret' --name 'kb2018_become_pass'
	kb2018_become_pass: !vault |
	          $ANSIBLE_VAULT;1.1;AES256
	          663 .... 462
	Encryption successful
	
Add user and encrypted password to /etc/ansible/host_vars/bs2020.yml
	
	root@kb2018:~# mkdir /etc/ansible/host_vars
	root@kb2018:~# nano /etc/ansible/host_vars/bs2020.yml
	bs2020_unprivilaged_user: kb2018
	bs2020_become_pass: !vault |
	          $ANSIBLE_VAULT;1.1;AES256
	          663 .... 462
	
Add variables to inventory
	
	[pets:children]
	servers
	containers
	
	[servers]
	kb2018   ansible_connection=local
	bs2020   ansible_host=bs2020.suspectdevices.com ansible_user='{{ bs2020_unprivilaged_user }}' ansible_become=yes ansible_become_user=root ansible_become_pass='{{ bs2020_become_pass }}'
	#bs2020   ansible_connection=ssh ansible_ssh_user=kb2018 
	
	[containers:children]
	local-containers
	remote-containers
	
	[local-containers]
	douglas ansible_connection=lxd
	...
	[remote-containers]
	...
	goethe  ansible_connection=lxd ansible_host=bs2020:goethe
	
	
And now we can treat all of our pets with the same love and affection.
	
	root@kb2018:~# ansible pets -m apt -a "force_apt_get=yes upgrade=yes update_cache=yes autoremove=yes" 
	

## References/Linkdump
* https://stackoverflow.com/questions/37297249/how-to-store-ansible-become-pass-in-a-vault-and-how-to-use-it
* https://docs.ansible.com/ansible/latest/user_guide/vault.html#id6