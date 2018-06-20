Infrared plugin to carry out migration from ML2OVS to OVN
=========================================================

This is an infrared plugin which can be used to carry out the migration
from ML2OVS to OVN if the tripleo was deployed using infrared.
See http://infrared.readthedocs.io/en/stable/index.html for more information.

Before using this plugin, first deploy an ML2OVS overcloud and then,

1. On your undercloud, install python-networking-ovn-migration-tool package (https://trunk.rdoproject.org/centos7-master/current/)
   You also need to install python-networking-ovn and python2-openvswitch packages.

2. Copy the folder networkin-ovn/migration/infrared/tripleo-ovn-migration into the infrared/plugins folder (this is a crude method. I need to figure out how to install this plugin properly)
2. Run
   $infrared plugin add plugins/tripleo-ovn-migration

3. Start migration by running

   $infrared  tripleo-ovn-migration  --version 13|14 \
--registry-namespace <REGISTRY_NAMESPACE> \
--registry-tag <TAG> \
--registry-prefix <PREFIX>

