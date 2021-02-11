# Systems Documentation
## Notes, and Things to be done.
[Operations Guide for current systems](OperationsGuide/) 

### Server Modernization Phase I

* Moving all legacy system functions onto separate linux containers isolated from each other.
* Use mirrored disk systems to insure that disk corruption does not lead to data corruption.
* Start giving a shit about the systems, code, and sites on them.
* Own your code/data. (If your free code hosting system is shutdown or taken over by Microsoft is it really free)
* Clean up the cruft (If it doesn't bring you joy DTMFA)
 
### Server Modernization Phase II
* Integrate Ansible into system maintenance tasks
* Reevaluate Centos and other RPM based containers built using playbooks vs profiles/scripts/cloud-init _while maintaining current security model_
* Develop off site backup strategy.

### SMP III _Make Shit Happen / Own Your Shit_
* Work on secure and efficient traffic in and out of home lans (Privoxy,DNS based ad blocking,squid etc) 
* Continue to refine server operation/maintanance.
* Build Gitlab and other alternatives to trac/git and evaluate workflows.
* Deploy off site backup strategy.
* Build out content. 
* Start new projects.
* Distribute data and backups over the network to home servers.
* [Document home server/network setup](edge-server-configuration/)
<!-- # Active Tickets
[[TicketQuery(status=new|assigned|accepted|reopened,order=id,desc=1,format=table,col=status|summary|owner|reporter)]]
-->
<!--## Recent Changes
[[RecentChanges(,5)]]
To make a complete copy of this site in either html or PDF  use this link. http://serverdocs.suspectdevices.com/serverdocs/admin/wikiprint/makebook
-->