<!-- NotesAddingAnsibleToContainerCreation, Version: 5, Modified: 2019/03/22, Author: feurig -->
## Adding Ansible to Container Creation
Container creation using ansible involved modifying some existing examples and tweaking things that worked using LXD and its cloud init. The result is the ability to create base containers with built in admin users and ssh key based connectivity. 

The system setup and admin user installation is done by the cloud-init portions of the susdev19 lxc profile. The network configuration is passed as part of creating the container.  The disk and network device was moved to a separate profile allowing containers to have different disk or network connections.  Because ansible requires python the create-lxd-containers playbook waits for cloud init to finish and then checks for python and attempts to install it if its not there.

All files used for ansible as well as the susdev19 lxc profile can be checked out of the private repository.

https://bitbucket.org/suspectdevicesadmin/ansible/src/master/

File layout.
* /etc/ansible/
* hosts/ -- base inventory file
* playlists/ -- playlists
* files/ -- files _(also where we put the profiles)_
* roles/

Currently this does not work to create containers on bs2020. To create a container on bs2020 
* create container on kb2018
* move the container to bs2020
* adjust the host file 

Things that needed to be changed in our current environment. 
* Profile needed to be broken out between network, system setup, and device mapping.
  * Network configuration is generated on the fly using a file or using ansible
  * User configuration and minimal software setup are now shared using the susdev19 profile
  * Default network devices and disk pools can be overridden using a separate profile _(infra for instance)_

* ansible vs cloud-init
  * Cloud init should provide a distro agnostic way to add users, keys and software.
  * Images do not always provide cloud init and even that may not be fully functional.
  * Ansible allows per distro scripting but not distro agnostic modules for many tasks

## Linkdump

* https://blog.sourcecode.de/posts/2016/11/25/how-to-create-lxd-containers-with-ansible-2-2/
* https://dev.to/livioribeiro/using-lxd-and-ansible-to-simulate-infrastructure-2g8l
* https://medium.com/@abhijeet.kamble619/10-things-you-should-start-using-in-your-ansible-playbook-808daff76b65
* https://leucos.github.io/ansible-files-layout
