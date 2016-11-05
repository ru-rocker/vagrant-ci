# vagrant-ci
Virtual machine for continous integration, based on CentOS 7

# Provisioning
The machine is provisioned by ansible. Therefore, you have to install ansible in your host machine.
Several software/tools are installed during executing ``vagrant up``
* git 
* ansible
* jdk (roles from ansible-galaxy: wiliamyeh.oracle-java. Adding checksum for JDK 8 only since I am using JDK 8)
* wildfly 
* jenkins (roles from ansible-galaxy: geerlingguy.jenkins. However I skip java installation since I am using Oracle JDK)
* maven

# Purpose
This virtual machine is intended only for continous integration demo for my colleagues, 
therefore if there are some hardcoded here and there, I am sorry :)
