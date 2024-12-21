#!/usr/bin/python3
#-----------------------------------------------------------ContainerShipData.py
# cs = ContainerShipData()
# cs.ansible_local_containers
# cs.ansible_remote_containers
# cs.local_active_containers
# cs.local_inactive_containers
# cs.remote_active_containers
# cs.remote_inactive_containers
# cs.spares
# cs.archives


INVENTORY_SOURCES='/etc/ansible/hosts'


from pylxd import Client as LXD
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import ansible_runner

import re
def escape_ansi(line):
     ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
     return ansi_escape.sub('', line)

from datetime import datetime as dt

class ContainerShipData:
  def __init__(self):
    self.ansible_local_containers = list(ansible_runner.interface.run(host_pattern='local_containers',
                                                                  module='ping',
                                                                  quiet=True,
                                                                  json_mode=True
                                                                 ).stats['processed'].keys()
                                         )

    self.ansible_remote_containers = list(ansible_runner.interface.run(host_pattern='remote_containers',
                                                                       module='ping',
                                                                       quiet=True,
                                                                       json_mode=True
                                                                      ).stats['processed'].keys()
                                         )

    # !!!! Lots of hard coded foo here .....
    self.bs2020 = LXD(endpoint='https://192.168.31.158:8443',cert=('/etc/ssl/certs/ssl-cert-snakeoil.pem','/etc/ssl/private/ssl-cert-snakeoil.key'),verify=False)
    self.kb2018 = LXD(endpoint='https://192.168.31.159:8443',cert=('/etc/ssl/certs/ssl-cert-snakeoil.pem','/etc/ssl/private/ssl-cert-snakeoil.key'),verify=False)

    self.local_active_containers=[]
    self.local_inactive_containers=[]
    for container in self.kb2018.containers.all():
       if container.status=='Running':
           self.local_active_containers.append(container.name)
       else:
           self.local_inactive_containers.append(container.name)

    self.remote_active_containers=[]
    self.remote_inactive_containers=[]
    self.spares={}

    for container in self.bs2020.containers.all():
       if container.status=='Running':
           self.remote_active_containers.append(container.name)
       else:
           if 'Spare-' not in container.name:
               self.remote_inactive_containers.append(container.name)
           else:
               containername=container.name.split('-')[1]
               containerdate=dt.strptime(container.created_at.split('T')[0],"%Y-%m-%d")
               if containername not in self.spares:
                   self.spares[containername]=[]
               self.spares[containername].append(containerdate)


    r=ansible_runner.interface.run(host_pattern='bs2020',
                                   module='command',
                                   module_args='/bin/ls -1 --color=none /archive',
                                   quiet=True)
    # this clusterfuck separates out the parts of the filenames and gets rid of the terminal cruft.
    archivelist=escape_ansi(r.stdout.read()).split('>>\n')[1].split('.tar.gz.tar\n')

    self.archives={}
    for archive in archivelist:
       if '-' in archive:
         aname,d=archive.split('-',1)
         adate=dt.strptime(d,"%Y-%m-%d")
         if aname not in self.archives:
             self.archives[aname]=[]
         self.archives[aname].append(adate)

    # its possible that these two should be moved to a separate script/module
    cull_spares={}
    for host in list(self.spares.keys()):
      if (len(self.spares[host]) > 2) :
         cull_spares[host]=self.spares[host][0:-2]
    self.spare_cullist=list(())
    for host in cull_spares:
      for doa in cull_spares[host]:
        self.spare_cullist.append('Spare-'+host+'-'+doa.strftime("%Y-%m-%d"))
    cull_archives={}
    for host in list(self.archives.keys()):
      if (len(self.archives[host]) > 2) :
         cull_archives[host]=self.archives[host][1:-1]
    self.archives_cullist=list(())
    for host in cull_archives:
      for doa in cull_archives[host]:
        self.archives_cullist.append(host+'-'+doa.strftime("%Y-%m-%d")+'.tar.gz.tar')

if __name__ == "__main__":
    cs = ContainerShipData()
    print("---local_containers:\n",cs.ansible_local_containers)
    print("---remote_containers:\n",cs.ansible_remote_containers)
    print("** According to LXD server kb2018 **")
    print("---local_active_containers----------------------------------------\n",
          cs.local_active_containers)
    print("---local_inactive_containers--------------------------------------\n",
          cs.local_inactive_containers)
    print("** According to LXD server bs2020 **")
    print("---remote_active_containers---------------------------------------\n",
          cs.remote_active_containers)
    print("---remote_inactive_containers-------------------------------------\n",
          cs.remote_inactive_containers)
    print("\n---Container spares on BS2020---------------------------------------")
    print(cs.spares)
    print("\n---Container archives on BS2020----------------------------------------")
    print(cs.archives)
    print("\n---Spares to delete on BS2020---------------------------------------")
    print (cs.spare_cullist)
    print("\n---Archives to delete on BS2020----------------------------------------")
    print (cs.archives_cullist)
