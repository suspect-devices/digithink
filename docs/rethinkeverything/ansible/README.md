# Anisible vs Puppet vs pylxd vs incus.
*THIS IS VERY MUCH A WORK IN PROGRESS*

Moving to incus pretty much broke the cloud.init+ansible pattern I developed when I started working with lxd. On the otherhand these patterns are pretty disfunctional *(unusable by others, tempermental, usw)*

## The point.
Looking at this provides the opportunity to do two things.

## Fix the pattern.

- Define what we are trying to achieve.
    - Update containers in our environment centrally.
    - Maintain the best security model.
        - for the colo
        - for the house lan
    - Look at alternative toolsets
    - test each of tool sets
        - Initialize and update containers with the tools/configurations we want universaly (python3, nano, ssh, usw/ssh-keys,admin user, usw)
        - Update the containers
- Impliment the desired outcomes using each of the tools based on the goals above.
- Select the best toolset and patterns and start using them. 
## Getting to it.
### Ansible and lxd.
### Use Cases.
### Initialization
### Ad Hoc Updates (ssh-keys root passwds usw)
