# susdevadmin/ansible
[https://bitbucket.org/suspectdevicesadmin/ansible/src/master/](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/)

This repository includes the inventory and playbooks for using ansible to manage lxd/lxc based containers as well as common files used to maintain suspect devices environment.

# Installing Ansible on lxd server.

[Notes On Installing Ansible](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/ServerInstall.md)
# Using Ansible.
## /etc/ansible/hosts
The hosts file serves to categorize and document the containers running on kb2018 and bs2020. 


## Ansible usage/playbook
### Using Ansible to update containers.
```
root@kb2018:/etc/ansible# ansible pets  -m raw -a "update.sh"
```
### Container Backup/Archive
*Ansible backups are DEPRECIATED.*

```
cd /etc/ansible ;screen -L time ansible-playbook playbooks/backup-lxd-containers.yml -vvv -i importants
```
A python based script which is run by cron at midnight maintains warm spares on bs2020:

```
/etc/ansible/python/NightlySnapshots.py
```
[https://bitbucket.org/suspectdevicesadmin/ansible/src/master/python/NightlySnapshots.py](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/python/NightlySnapshots.py)

### Creation of containers
Container creation is simply a matter of adding the container info to [/etc/ansible/hosts](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/hosts). under local_containers. 

```
root@kb2018:/etc/ansible# nano hosts
...
#   variables used by playbooks to create/maintain containers
#   Host Variables
#     ip_address
#     purpose #
#   Lan Variables
#     ip_netmask
#     ip_gateway
#     ip_dns_server (default server)
#   Base Image alias to create container
#     image_alias
#   Profiles
#     net_and_disk_profile - profile defining disk pool and network connection
#     system_profile       - base users and other cloud-config items
...
[local_containers]
...
 agoodauthor ip_address=198.202.31.160 purpose="Sample Server" image_alias="ubuntu/focal/cloud"  
...

```
Then run the [create-lxc-containers](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/roles/create_lxd_containers/tasks/main.yml) playbook.

```
root@kb2018:/etc/ansible# ansible-playbook playbooks/create-lxd-containers.yml 
```

### Making your changes perminant

Perminant modifications to this directory should be followed by 

```
git commit -a m"Reason for change"
git push.
```
