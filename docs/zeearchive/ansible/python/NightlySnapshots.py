#!/usr/bin/python3
#------------------------------------------------------------NightlySnapshots.py
# Snapshot container and move it to the other server.
# then cleanup extra Snapshots/Spare Containers.
# The idea here is to have a warm spare no more than 24hrs old.
#
# (c)2020-2021 D Delmar Davis, Suspect Devices. All rights reserved.
#
# root@kb2018:/etc/ansible# chmod +x /etc/ansible/python/NightlySnapshots.py
# @midnight /path/to/NightlySnapshots.py
# Note this does not archive the snapshots.
from datetime import datetime

start_time=datetime.now()
t = datetime.now().strftime("%Y-%m-%d")

import warnings
warnings.simplefilter("ignore")

from ContainerShipData import ContainerShipData
print ('...gathering Container Data ',start_time.strftime('%H:%M:%S'),'...')
susdev=ContainerShipData()

import ansible_runner

for h in susdev.local_active_containers:
   c=susdev.kb2018.containers.get(h)

   print('...checking for snapshot '+h+'/'+t,end=' ')
   try:
      s=c.snapshots.get(t)
      print('... Found one: ...\n* deleting ...')
      s.delete(wait=True)
   except:
       print ('... none found ...')

   s=c.snapshots.create(t,stateful=False,wait=True)

   # check for existing Spare
   for cs in susdev.bs2020.containers.all():
      if 'Spare-'+h+'-'+t in cs.name:
          print('...found bs2020:Spare-'+h+'-'+t+'...\n* deleting ...')
          cs.delete(wait=True)
   # none of the apis allow moving snapshots to containers so we call lxd directly
   # TODO: check to make sure it was successful.
   # also consider replacing runner with a command pipe.
   thetrick='lxc move '+h+'/'+t+' bs2020:Spare-'+h+'-'+t
   print('* ',thetrick,'...')
   r=ansible_runner.interface.run(host_pattern='kb2018',module='command',module_args=thetrick,quiet=True)

   for cs in susdev.bs2020.containers.all():
      if 'Spare-'+h in cs.name:
          cs.stop()
          if '-'+t not in cs.name:
              cs.delete()
end_time=datetime.now()

print('... finished',end_time.strftime('%H:%M:%S'),'...')
print('...elapsed time',end_time-start_time,'...')

# todo: set alternate inventory source.
