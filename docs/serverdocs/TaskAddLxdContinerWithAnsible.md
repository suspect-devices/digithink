<!-- TaskAddLxdContinerWithAnsible, Version: 9, Modified: 2019/03/23, Author: feurig -->
## New Container Using Ansible 

With Ansible added to kb2018 we expand on the profiles we use to create users and create a sane environment. There are two steps required to create a container on kb2018. 

1. Add the name, ip_address, and purpose to the inventory file _/etc/ansible/hosts_.

```sh
...
redshirt ip_address=198.202.31.200 purpose="Disposable Ubuntu"
...

2. Run the ansible playbook _/etc/ansible/playbooks/create-lxd-containers.yml_

root@kb2018:/etc/ansible# ansible-playbook /etc/ansible/playbooks/create-lxd-containers.yml

PLAY [localhost] ********************************************************************************************************************************************************************
```

If you want something other than ubuntu-lts you can:
* set the image_alias. _these are images that we know work in our environment_

```sh
root@kb2018:/etc/ansible# lxc image list
+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
|   ALIAS    | FINGERPRINT  | PUBLIC |                 DESCRIPTION                 |  ARCH  |   SIZE   |          UPLOAD DATE          |
+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
| centos/7c  | 700c86f31546 | no     | Centos 7 (20190109_02:16) plus cloud        | x86_64 | 172.49MB | Mar 21, 2019 at 1:54am (UTC)  |
+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
| debian/9c  | 38d17964647d | no     | Debian stretch (20190108_05:24) plus cloud  | x86_64 | 227.58MB | Mar 19, 2019 at 5:57am (UTC)  |
+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
| ubuntu-lts | c395a7105278 | no     | ubuntu 18.04 LTS amd64 (release) (20180911) | x86_64 | 173.98MB | Sep 29, 2018 at 11:50pm (UTC) |
+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
root@kb2018:~# cd /etc/ansible/
root@kb2018:/etc/ansible# ls
ansible.cfg  files  hosts  host_vars  playbooks  README.md  roles
oot@kb2018:/etc/ansible# lxc delete redshirt --force
root@kb2018:/etc/ansible# nano hosts 
...
redshirt ip_address=198.202.31.200 purpose="Disposable Debian" image_alias="debian/9c"
...

And (re)run the playbook.

root@kb2018:/etc/ansible# ansible-playbook /etc/ansible/playbooks/create-lxd-containers.yml
```	

You can also create infrastructure servers by setting net_and_disk_profile to "infra".

The ansible playbook and host file are maintained in a private bitbucket repository. If you add roles or create a host that you want to keep please update the repository.  _Ignore the errors, I will reconfigure a user for kb2018 when bitbucket really stops supporting the organization account_
```sh	
feurig@kb2018:~$ sudo bash
[sudo] password for feurig: 
root@kb2018:~# cd /etc/ansible/hosts
root@kb2018:/etc/ansible# nano hosts
...
morgan   ip_address=198.202.31.224 purpose="Infrastucture Test Machine" net_and_disk_profile="infra"
...
root@kb2018:/etc/ansible# ansible-playbook /etc/ansible/playbooks/create-lxd-containers.yml 
PLAY RECAP **************************************************************************************************************************************************************************
localhost                  : ok=4    changed=1    unreachable=0    failed=0   

root@kb2018:/etc/ansible# git commit -a -m "Recreate Morgan as Infrastructure Test Server"
[master 10d4ce0] Recreate Morgan as Infrastructure Test Server
	Committer: Root at KB2018 <root@kb2018.suspectdevices.com>
...
	1 file changed, 1 insertion(+), 1 deletion(-)
root@kb2018:/etc/ansible# git push
Counting objects: 3, done.
Delta compression using up to 16 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 378 bytes | 378.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0)
remote: 
remote: Warning!
remote: You are currently connecting with your team account.
remote: This is no longer supported, so please connect using your user account.
remote: 
To bitbucket.org:suspectdevicesadmin/ansible.git
	d7f5f12..10d4ce0  master -> master
root@kb2018:/etc/ansible# 
```