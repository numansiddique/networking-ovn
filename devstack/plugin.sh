#!/bin/bash

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# devstack/plugin.sh
# networking-ovn actions for devstack plugin framework

# Save trace setting
_XTRACE_OVN_PLUGIN=$(set +o | grep xtrace)
set +o xtrace
source $DEST/networking-ovn/devstack/lib/networking-ovn
source $TOP_DIR/lib/neutron-legacy

# main loop
if is_service_enabled q-svc || is_service_enabled ovn-northd || is_service_enabled ovn-controller || is_service_enabled ovn-controller-vtep ; then
    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        install_ovn
        configure_ovn
        init_ovn
        # We have to start at install time, because Neutron's post-config
        # phase runs ovs-vsctl.
        start_ovs
        disable_libvirt_apparmor
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        configure_ovn_plugin

        if is_service_enabled nova; then
            create_nova_conf_neutron
        fi

        start_ovn

        # If not previously set by another process, set the OVN_*_DB
        # variables to enable OVN commands from any node.
        grep -lq 'OVN' ~/.bash_profile || echo -e "\n# Enable OVN commands from any node.\nexport OVN_NB_DB=$OVN_NB_REMOTE\nexport OVN_SB_DB=$OVN_SB_REMOTE" >> ~/.bash_profile

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        if [[ "$OVN_L3_CREATE_PUBLIC_NETWORK" == "True" ]]; then
            if [[ "$NEUTRON_CREATE_INITIAL_NETWORKS" != "True" ]]; then
                echo "OVN_L3_CREATE_PUBLIC_NETWORK=True is being ignored because"
                echo "NEUTRON_CREATE_INITIAL_NETWORKS is set to False"
            else
                create_public_bridge
            fi
        fi
    fi

    if [[ "$1" == "unstack" ]]; then
        stop_ovn
        stop_ovs_dp
        cleanup_ovn
    fi
fi

if is_service_enabled ovn-octavia; then
    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing octavia with ovn provider driver"
        install_ovn_octavia
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring octavia with ovn provider driver"
        configure_ovn_octavia
    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        start_ovn_octavia
    fi

    if [[ "$1" == "unstack" ]]; then
        echo_summary "Uninstalling octavia with ovn provider driver"
        stop_ovn_octavia
    fi
fi
# Restore xtrace
$_XTRACE_OVN_PLUGIN

# Tell emacs to use shell-script-mode
## Local variables:
## mode: shell-script
## End:
