# Using python to directly interact with LXD and Ansible.
Using ansible to create and backup containers is kind of a shitpile *(which is weird because the debian installable pylxd interface looks really good)*. Some of the side effects of our attempts to use ansible to back up our containers included snapshots (which had to be manually culled) running at the same ip as the production servers.

For this reason I plan to directly run container creation backup and migration from python (v3). Python scripts should reference the same datasource for which servers are which. My original foray into ansibles internal and poorly documented api felt about as painfull as the ansible itself. I replaced it with ansible_runner.

These modules are intended to be usefull standalone or as part of a maintainance routine. 

## Module ContainerShipData
### Ansible data
* ansible_local_containers
* ansible_remote_containers

### According to LXD server kb2018 
* kb2018_local_active_containers
* kb2018_local_inactive_containers

### According to LXD server bs2020
* kb2018_remote_active_containers
* kb2018_remote_inactive_containers
* snapshots
* archives

#### Cull Lists
* snapshot_cullist
* archives_cullist

## REFERENCES:
* [https://www.programcreek.com/python/example/90872/ansible.parsing.dataloader.DataLoader](https://www.programcreek.com/python/example/90872/ansible.parsing.dataloader.DataLoader)
* [https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
](https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
) 
* [https://www.programcreek.com/python/example/111311/ansible.inventory.manager.InventoryManager](https://www.programcreek.com/python/example/111311/ansible.inventory.manager.InventoryManager)  