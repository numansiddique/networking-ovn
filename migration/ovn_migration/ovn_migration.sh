#!/bin/bash

# With LANG set to everything else than C completely undercipherable errors
# like "file not found" and decoding errors will start to appear during scripts
# or even ansible modules
LANG=C

# Complete stackrc file path.
STACKRC_FILE=${STACKRC_FILE:-~/stackrc}

# Complete overcloudrc file path.
OVERCLOUDRC_FILE=${OVERCLOUDRC_FILE:-~/overcloudrc}

# overcloud deploy script for OVN migration.
OVERCLOUD_OVN_DEPLOY_FILE=${OVERCLOUD_OVN_DEPLOY_FILE:-~/overcloud_deploy_ovn.sh}

GENEVE_MTU_SIZE=${GENEVE_MTU_SIZE:-1440}

# Is the present deployment DVR or HA. Lets assume it's HA
IS_DVR_ENABLED=${IS_DVR_ENABLED:-False}

IS_TRIPLEO_DEPLOYMENT=${IS_TRIPLEO_DEPLOYMENT:-True}

: ${OPT_WORKDIR:=$HOME/ovn_migration}

PUBLIC_NETWORK_NAME=${PUBLIC_NETWORK_NAME:-public}

CREATE_MIGRATION_RESOURCES=${CREATE_MIGRATION_RESOURCES:-True}

# Check if the neutron networks MTU has been updated to geneve MTU size or not.
# We donot want to proceed if the MTUs are not updated.
oc_check_network_mtu() {
    source $OVERCLOUDRC_FILE
    python network_mtu.py check mtu $GENEVE_MTU_SIZE
    if [ "$?" != "0" ]
    then
        echo "Please update the tenant network MTU by running 'python network_mtu.py update mtu 1440' before starting migration"
        exit 1
    fi
}

generate_ansible_hosts_file() {
    source $STACKRC_FILE
    CONTROLLERS=`nova list --fields name,networks | grep controller     | \
    awk -e '{ split($6, net, "="); printf "%s.localdomain=%s\n", $4, net[2] }'`
    echo "[ovn-dbs]"  > hosts_for_migration
    for rec in $CONTROLLERS;
    do
        rec_array=(${rec//=/ })
        node_hostname=${rec_array[0]}
        node_ip=${rec_array[1]}
        echo $node_ip >> hosts_for_migration
    done

    echo "" >> hosts_for_migration
    echo "[ovn-controllers]" >> hosts_for_migration
    for rec in $CONTROLLERS;
    do
        rec_array=(${rec//=/ })
        node_hostname=${rec_array[0]}
        node_ip=${rec_array[1]}
        echo $node_ip >> hosts_for_migration
    done
    COMPUTES=`nova list --fields name,networks |  grep compute | \
    awk -e '{ split($6, net, "="); printf "%s.localdomain=%s\n", $4, net[2] }'`
    for rec in $COMPUTES;
    do
        rec_array=(${rec//=/ })
        node_hostname=${rec_array[0]}
        node_ip=${rec_array[1]}
        echo $node_ip >> hosts_for_migration
    done

    echo "" >> hosts_for_migration

    cat >> hosts_for_migration << EOF
[overcloud:children]
ovn-controllers
ovn-dbs

[overcloud:vars]
remote_user=heat-admin
dvr_setup=$IS_DVR_ENABLED
tripleo_deployment=$IS_TRIPLEO_DEPLOYMENT
public_network_name=$PUBLIC_NETWORK_NAME
create_migration_resources=$CREATE_MIGRATION_RESOURCES
working_dir=$OPT_WORKDIR
EOF
}

# Step 1. Check if the user has generated overcloud-deploy-ovn.sh file
# If it is not generated. Exit
if [ ! -e $OVERCLOUD_OVN_DEPLOY_FILE ]
then
    echo "overcloud deploy migration scrip : $OVERCLOUD_OVN_DEPLOY_FILE is not present. Please make sure you generate that file before running this"
    exit 1     
fi

oc_check_network_mtu

# Generate the hosts file for ansible migration playbook.
generate_ansible_hosts_file

# Lets kick start the ansible playbook.
echo "Starting the Migration"
ansible-playbook  $OPT_WORKDIR/playbooks/ovn-migration.yml \
    -i hosts_for_migration
