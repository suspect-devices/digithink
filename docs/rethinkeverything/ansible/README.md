# Anisible vs Puppet vs pylxd vs incus.
*THIS IS VERY MUCH A WORK IN PROGRESS*

Moving to incus pretty much broke the cloud.init+ansible pattern I developed when I started working with lxd. On the otherhand these patterns are pretty disfunctional *(unusable by others, tempermental, usw)*

## The point.
Looking at this provides the opportunity to do two things.

1. Fix the pattern.

    1. Look at alternative toolsets
    2. Define what we are trying to achieve.
        1. Update containers in our environment centrally.
        2. Maintain the best security model.
        3. Initialize containers with the tools/configurations we want universally (python3, nano, ssh, usw/ssh-keys,admin user, usw)
    3. Impliment the desired outcomes using each of the tools based on the goals above.
    4. Select the best toolset and patterns. 
## Getting to it.
### Ansible and lxd.
### Use Cases.
### Initialization
### Ad Hoc Updates (ssh-keys root passwds usw)
