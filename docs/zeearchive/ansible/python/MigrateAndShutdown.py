#!/usr/bin/python3
#------------------------------------------------------------MigrateAndShutdown.py
# Snapshot and shutdown container and move it to the other server.
# then rename it and runup the snapshot.
# This is in preperation to shutdown the main server.
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

# Wish this was more usefull. !!#@$!! ANSIBLE
import ansible_runner

for h in susdev.local_active_containers:
   c=susdev.kb2018.containers.get(h)

   print('...checking for snapshot '+h+'/'+t)
   try:
      s=c.snapshots.get(t)
      print('... Found one:...\n* deleting ...')
      s.delete(wait=True)
   except:
       print ('...none found...')

   s=c.snapshots.create(t,stateful=False,wait=True)
   # check for existing Spare
   for cs in susdev.bs2020.containers.all():
      if 'Spare-'+h+'-'+t in cs.name:
          print('...found existing bs2020:Spare-'+h+'-'+t+'...\n* deleting ...')
          cs.delete(wait=True)

   # none of the apis allow moving snapshots to containers so we call lxd directly
   # TODO: check to make sure it was successful.
   # also consider replacing runner with a command pipe.
   thetrick='lxc move '+h+'/'+t+' bs2020:Spare-'+h+'-'+t
   print('*',thetrick,'...')
   r=ansible_runner.interface.run(host_pattern='kb2018',module='command',module_args=thetrick,quiet=True)

   c.stop()

   for cs in susdev.bs2020.containers.all():
      if 'Spare-'+h+'-'+t in cs.name:
        print('....Found Spare-'+h+'-'+t,'...\n* Starting!')
        cs.start()

   for cs in susdev.kb2018.containers.all():
     if 'Old-'+h in cs.name:
             print('...found existing Old-'+h+'...\n* deleting ...')
             #cs.delete(wait=True)
             cs.rename('Old-CMA-'+h)
   print('Rename '+h+' to Old-'+h)
   c.rename('Old-'+h)

end_time=datetime.now()

print('... finished',end_time.strftime('%H:%M:%S'),'...')
print('...elapsed time',end_time-start_time,'...')

# todo: set alternate inventory source.
