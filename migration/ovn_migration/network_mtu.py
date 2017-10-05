from openstack import connection
import os
import sys

def get_connection():
    conn = connection.Connection(auth_url=os.environ['OS_AUTH_URL'],
                                 project_name=os.environ['OS_PROJECT_NAME'],
                                 username=os.environ['OS_USERNAME'],
                                 password=os.environ['OS_PASSWORD'])
    return conn


def verify_network_mtus(mtu):
    conn = get_connection()
    for network in conn.network.networks():
        if network.provider_physical_network is not None:
            if network.mtu != mtu:
                return False
    return True



def update_network_mtu(mtu_to_update):
    conn = get_connection()
    for net in conn.network.networks():
        try:
            if net.provider_physical_network is not None:
                if net.provider_network_type == 'vxlan' and (
                        net.mtu != mtu_to_update):
                    conn.network.update_network(net, mtu=mtu_to_update)
        except Exception as e:
            print("Exception occured while updating the MTU", e)
            raise



if len(sys.argv) < 4:
    sys.exit(1)

retval = 1
if sys.argv[1] == "update" and sys.argv[2] == "mtu":
    retval = update_network_mtu(sys.argv[3])
elif sys.argv[1] == "check" and sys.argv[2] == "mtu":
    retval = verify_network_mtus(sys.argv[3])

sys.exit(retval)
