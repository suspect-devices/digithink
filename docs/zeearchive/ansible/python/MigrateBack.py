#!/usr/bin/python3
#-----------------------------------------------------------------MigrateBack.py
# Move Spares back to main server.
# THIS NEEDS WORK.
#
# (c)2020-2021 D Delmar Davis, Suspect Devices. All rights reserved.
#
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

for h in susdev.remote_active_containers:
   c=susdev.bs2020.containers.get(h)
   if 'Spare-' in c.name:
       n=c.name.split('-')[1]
       print ('* restoring '+n+'...')
   else:
       continue

   print('...checking for snapshot '+c.name+'/'+t+'...')
   try:
      s=c.snapshots.get(t)
      print('... Found one:...\n* deleting ...')
      s.delete(wait=True)
   except:
       print ('...none found...')

   s=c.snapshots.create(t,stateful=False,wait=True)
   # check for existing container.
   #for cs in susdev.kb2018.containers.all()
   #      if +t in cs.name:
   #      print('...found existing '+n+'-'+t+'...\n* deleting ...')
   #      cs.delete(wait=True) # probably should rename to cma.

   # none of the apis allow moving snapshots to containers so we call lxd directly
   # TODO: check to make sure it was successful.
   # also consider replacing runner with a command pipe.
   thetrick='lxc copy bs2020:'+c.name+'/'+t+' '+n
   print('*',thetrick,'...')
   r=ansible_runner.interface.run(host_pattern='kb2018',module='command',module_args=thetrick,quiet=True)

   c.stop()

   for cs in susdev.kb2018.containers.all():
      if ':'+n+':' in ':'+cs.name+':':
        print('....Found '+n+'...\n* Starting!')
        cs.start()

#   for cs in susdev.kb2018.containers.all():
#     if 'Old-'+h in cs.name:
#             print('...found existing Old-'+h+'...\n* deleting ...')
#             #cs.delete(wait=True)
#             cs.rename('Old-CMA-'+h)
#   print('Rename '+h+' to Old-'+h)
#   c.rename('Old-'+h)

end_time=datetime.now()

print('... finished',end_time.strftime('%H:%M:%S'),'...')
print('...elapsed time',end_time-start_time,'...')

# todo: set alternate inventory source.
