#
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
#

import copy
import mock

from networking_ovn.common import constants as ovn_const
from networking_ovn.common import utils
from networking_ovn.ovsdb import impl_idl_ovn
from networking_ovn.tests import base
from networking_ovn.tests.unit import fakes


class TestDBImplIdlOvn(base.TestCase):

    def _load_ovsdb_fake_rows(self, table, fake_attrs):
        for fake_attr in fake_attrs:
            fake_row = fakes.FakeOvsdbRow.create_one_ovsdb_row(
                attrs=fake_attr)
            # Pre-populate ovs idl "._data"
            fake_data = copy.deepcopy(fake_attr)
            try:
                del fake_data["unit_test_id"]
            except KeyError:
                pass
            setattr(fake_row, "_data", fake_data)
            table.rows[fake_row.uuid] = fake_row

    def _find_ovsdb_fake_row(self, table, key, value):
        for fake_row in table.rows.values():
            if getattr(fake_row, key) == value:
                return fake_row
        return None

    def _construct_ovsdb_references(self, fake_associations,
                                    parent_table, child_table,
                                    parent_key, child_key,
                                    reference_column_name):
        for p_name, c_names in fake_associations.items():
            p_row = self._find_ovsdb_fake_row(parent_table, parent_key, p_name)
            c_uuids = []
            for c_name in c_names:
                c_row = self._find_ovsdb_fake_row(child_table, child_key,
                                                  c_name)
                if not c_row:
                    continue
                # Fake IDL processing (uuid -> row)
                c_uuids.append(c_row)
            setattr(p_row, reference_column_name, c_uuids)


class TestNBImplIdlOvn(TestDBImplIdlOvn):

    fake_set = {
        'lswitches': [
            {'name': utils.ovn_name('ls-id-1'),
             'external_ids': {ovn_const.OVN_NETWORK_NAME_EXT_ID_KEY:
                              'ls-name-1'}},
            {'name': utils.ovn_name('ls-id-2'),
             'external_ids': {ovn_const.OVN_NETWORK_NAME_EXT_ID_KEY:
                              'ls-name-2'}},
            {'name': utils.ovn_name('ls-id-3'),
             'external_ids': {ovn_const.OVN_NETWORK_NAME_EXT_ID_KEY:
                              'ls-name-3'}},
            {'name': 'ls-id-4',
             'external_ids': {'not-neutron:network_name': 'ls-name-4'}},
            {'name': utils.ovn_name('ls-id-5'),
             'external_ids': {ovn_const.OVN_NETWORK_NAME_EXT_ID_KEY:
                              'ls-name-5'}}],
        'lswitch_ports': [
            {'name': 'lsp-id-11', 'addresses': ['10.0.1.1'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-11'}},
            {'name': 'lsp-id-12', 'addresses': ['10.0.1.2'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-12'}},
            {'name': 'lsp-rp-id-1', 'addresses': ['10.0.1.254'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-rp-name-1'},
             'options': {'router-port':
                         utils.ovn_lrouter_port_name('orp-id-a1')}},
            {'name': 'lsp-id-21', 'addresses': ['10.0.2.1'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-21'}},
            {'name': 'lsp-id-22', 'addresses': ['10.0.2.2'],
             'external_ids': {}},
            {'name': 'lsp-id-23', 'addresses': ['10.0.2.3'],
             'external_ids': {'not-neutron:port_name': 'lsp-name-23'}},
            {'name': 'lsp-rp-id-2', 'addresses': ['10.0.2.254'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-rp-name-2'},
             'options': {'router-port':
                         utils.ovn_lrouter_port_name('orp-id-a2')}},
            {'name': 'lsp-id-31', 'addresses': ['10.0.3.1'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-31'}},
            {'name': 'lsp-id-32', 'addresses': ['10.0.3.2'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-32'}},
            {'name': 'lsp-rp-id-3', 'addresses': ['10.0.3.254'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-rp-name-3'},
             'options': {'router-port':
                         utils.ovn_lrouter_port_name('orp-id-a3')}},
            {'name': 'lsp-vpn-id-3', 'addresses': ['10.0.3.253'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-vpn-name-3'}},
            {'name': 'lsp-id-41', 'addresses': ['20.0.1.1'],
             'external_ids': {'not-neutron:port_name': 'lsp-name-41'}},
            {'name': 'lsp-rp-id-4', 'addresses': ['20.0.1.254'],
             'external_ids': {},
             'options': {'router-port': 'xrp-id-b1'}},
            {'name': 'lsp-id-51', 'addresses': ['20.0.2.1'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-51'}},
            {'name': 'lsp-id-52', 'addresses': ['20.0.2.2'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-name-52'}},
            {'name': 'lsp-rp-id-5', 'addresses': ['20.0.2.254'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-rp-name-5'},
             'options': {'router-port':
                         utils.ovn_lrouter_port_name('orp-id-b2')}},
            {'name': 'lsp-vpn-id-5', 'addresses': ['20.0.2.253'],
             'external_ids': {ovn_const.OVN_PORT_NAME_EXT_ID_KEY:
                              'lsp-vpn-name-5'}}],
        'lrouters': [
            {'name': utils.ovn_name('lr-id-a'),
             'external_ids': {ovn_const.OVN_ROUTER_NAME_EXT_ID_KEY:
                              'lr-name-a'},
             'options': {'chassis': 'host-1'}},
            {'name': utils.ovn_name('lr-id-b'),
             'external_ids': {ovn_const.OVN_ROUTER_NAME_EXT_ID_KEY:
                              'lr-name-b'},
             'options': {'chassis': 'host-1'}},
            {'name': utils.ovn_name('lr-id-c'),
             'external_ids': {ovn_const.OVN_ROUTER_NAME_EXT_ID_KEY:
                              'lr-name-c'},
             'options': {'chassis': 'host-2'}},
            {'name': utils.ovn_name('lr-id-d'),
             'external_ids': {ovn_const.OVN_ROUTER_NAME_EXT_ID_KEY:
                              'lr-name-d'},
             'options': {'chassis': ovn_const.OVN_GATEWAY_INVALID_CHASSIS}},
            {'name': utils.ovn_name('lr-id-e'),
             'external_ids': {ovn_const.OVN_ROUTER_NAME_EXT_ID_KEY:
                              'lr-name-e'},
             'options': {}}],
        'lrouter_ports': [
            {'name': utils.ovn_lrouter_port_name('orp-id-a1'),
             'external_ids': {}, 'networks': ['10.0.1.0/24']},
            {'name': utils.ovn_lrouter_port_name('orp-id-a2'),
             'external_ids': {}, 'networks': ['10.0.2.0/24']},
            {'name': utils.ovn_lrouter_port_name('orp-id-a3'),
             'external_ids': {}, 'networks': ['10.0.3.0/24']},
            {'name': 'xrp-id-b1',
             'external_ids': {}, 'networks': ['20.0.1.0/24']},
            {'name': utils.ovn_lrouter_port_name('orp-id-b2'),
             'external_ids': {}, 'networks': ['20.0.2.0/24']}],
        'static_routes': [{'ip_prefix': '20.0.0.0/16',
                           'nexthop': '10.0.3.253'},
                          {'ip_prefix': '10.0.0.0/16',
                           'nexthop': '20.0.2.253'}],
        'acls': [
            {'unit_test_id': 1,
             'action': 'allow-related', 'direction': 'from-lport',
             'external_ids': {'neutron:lport': 'lsp-id-11'},
             'match': 'inport == "lsp-id-11" && ip4'},
            {'unit_test_id': 2,
             'action': 'allow-related', 'direction': 'to-lport',
             'external_ids': {'neutron:lport': 'lsp-id-11'},
             'match': 'outport == "lsp-id-11" && ip4.src == $as_ip4_id_1'},
            {'unit_test_id': 3,
             'action': 'allow-related', 'direction': 'from-lport',
             'external_ids': {'neutron:lport': 'lsp-id-12'},
             'match': 'inport == "lsp-id-12" && ip4'},
            {'unit_test_id': 4,
             'action': 'allow-related', 'direction': 'to-lport',
             'external_ids': {'neutron:lport': 'lsp-id-12'},
             'match': 'outport == "lsp-id-12" && ip4.src == $as_ip4_id_1'},
            {'unit_test_id': 5,
             'action': 'allow-related', 'direction': 'from-lport',
             'external_ids': {'neutron:lport': 'lsp-id-21'},
             'match': 'inport == "lsp-id-21" && ip4'},
            {'unit_test_id': 6,
             'action': 'allow-related', 'direction': 'to-lport',
             'external_ids': {'neutron:lport': 'lsp-id-21'},
             'match': 'outport == "lsp-id-21" && ip4.src == $as_ip4_id_2'},
            {'unit_test_id': 7,
             'action': 'allow-related', 'direction': 'from-lport',
             'external_ids': {'neutron:lport': 'lsp-id-41'},
             'match': 'inport == "lsp-id-41" && ip4'},
            {'unit_test_id': 8,
             'action': 'allow-related', 'direction': 'to-lport',
             'external_ids': {'neutron:lport': 'lsp-id-41'},
             'match': 'outport == "lsp-id-41" && ip4.src == $as_ip4_id_4'},
            {'unit_test_id': 9,
             'action': 'allow-related', 'direction': 'from-lport',
             'external_ids': {'neutron:lport': 'lsp-id-52'},
             'match': 'inport == "lsp-id-52" && ip4'},
            {'unit_test_id': 10,
             'action': 'allow-related', 'direction': 'to-lport',
             'external_ids': {'neutron:lport': 'lsp-id-52'},
             'match': 'outport == "lsp-id-52" && ip4.src == $as_ip4_id_5'}],
        'dhcp_options': [
            {'cidr': '10.0.1.0/24',
             'external_ids': {'subnet_id': 'subnet-id-10-0-1-0'},
             'options': {'mtu': '1442', 'router': '10.0.1.254'}},
            {'cidr': '10.0.2.0/24',
             'external_ids': {'subnet_id': 'subnet-id-10-0-2-0'},
             'options': {'mtu': '1442', 'router': '10.0.2.254'}},
            {'cidr': '10.0.3.0/24',
             'external_ids': {'subnet_id': 'subnet-id-10-0-3-0',
                              'port_id': 'lsp-vpn-id-3'},
             'options': {'mtu': '1442', 'router': '10.0.3.254'}},
            {'cidr': '20.0.1.0/24',
             'external_ids': {'subnet_id': 'subnet-id-20-0-1-0'},
             'options': {'mtu': '1442', 'router': '20.0.1.254'}},
            {'cidr': '20.0.2.0/24',
             'external_ids': {'subnet_id': 'subnet-id-20-0-2-0',
                              'port_id': 'lsp-vpn-id-5'},
             'options': {'mtu': '1442', 'router': '20.0.2.254'}},
            {'cidr': '2001:dba::/64',
             'external_ids': {'subnet_id': 'subnet-id-2001-dba',
                              'port_id': 'lsp-vpn-id-5'},
             'options': {'server_id': '12:34:56:78:9a:bc'}},
            {'cidr': '30.0.1.0/24',
             'external_ids': {'port_id': 'port-id-30-0-1-0'},
             'options': {'mtu': '1442', 'router': '30.0.2.254'}},
            {'cidr': '30.0.2.0/24', 'external_ids': {}, 'options': {}}],
        'address_sets': [
            {'name': '$as_ip4_id_1',
             'addresses': ['10.0.1.1', '10.0.1.2'],
             'external_ids': {ovn_const.OVN_SG_NAME_EXT_ID_KEY: 'id_1'}},
            {'name': '$as_ip4_id_2',
             'addresses': ['10.0.2.1'],
             'external_ids': {ovn_const.OVN_SG_NAME_EXT_ID_KEY: 'id_2'}},
            {'name': '$as_ip4_id_3',
             'addresses': ['10.0.3.1', '10.0.3.2'],
             'external_ids': {ovn_const.OVN_SG_NAME_EXT_ID_KEY: 'id_3'}},
            {'name': '$as_ip4_id_4',
             'addresses': ['20.0.1.1', '20.0.1.2'],
             'external_ids': {}},
            {'name': '$as_ip4_id_5',
             'addresses': ['20.0.2.1', '20.0.2.2'],
             'external_ids': {ovn_const.OVN_SG_NAME_EXT_ID_KEY: 'id_5'}},
            ]}

    fake_associations = {
        'lstolsp': {
            utils.ovn_name('ls-id-1'): [
                'lsp-id-11', 'lsp-id-12', 'lsp-rp-id-1'],
            utils.ovn_name('ls-id-2'): [
                'lsp-id-21', 'lsp-id-22', 'lsp-id-23', 'lsp-rp-id-2'],
            utils.ovn_name('ls-id-3'): [
                'lsp-id-31', 'lsp-id-32', 'lsp-rp-id-3', 'lsp-vpn-id-3'],
            'ls-id-4': [
                'lsp-id-41', 'lsp-rp-id-4'],
            utils.ovn_name('ls-id-5'): [
                'lsp-id-51', 'lsp-id-52', 'lsp-rp-id-5', 'lsp-vpn-id-5']},
        'lrtolrp': {
            utils.ovn_name('lr-id-a'): [
                utils.ovn_lrouter_port_name('orp-id-a1'),
                utils.ovn_lrouter_port_name('orp-id-a2'),
                utils.ovn_lrouter_port_name('orp-id-a3')],
            utils.ovn_name('lr-id-b'): [
                'xrp-id-b1',
                utils.ovn_lrouter_port_name('orp-id-b2')]},
        'lrtosroute': {
            utils.ovn_name('lr-id-a'): ['20.0.0.0/16'],
            utils.ovn_name('lr-id-b'): ['10.0.0.0/16']
            },
        'lstoacl': {
            utils.ovn_name('ls-id-1'): [1, 2, 3, 4],
            utils.ovn_name('ls-id-2'): [5, 6],
            'ls-id-4': [7, 8],
            utils.ovn_name('ls-id-5'): [9, 10]}
        }

    def setUp(self):
        super(TestNBImplIdlOvn, self).setUp()

        self.lswitch_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.lsp_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.lrouter_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.lrp_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.sroute_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.acl_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.dhcp_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self.address_set_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()

        self._tables = {}
        self._tables['Logical_Switch'] = self.lswitch_table
        self._tables['Logical_Switch_Port'] = self.lsp_table
        self._tables['Logical_Router'] = self.lrouter_table
        self._tables['Logical_Router_Port'] = self.lrp_table
        self._tables['Logical_Router_Static_Route'] = self.sroute_table
        self._tables['ACL'] = self.acl_table
        self._tables['DHCP_Options'] = self.dhcp_table
        self._tables['Address_Set'] = self.address_set_table

        with mock.patch.object(impl_idl_ovn, 'get_connection',
                               return_value=mock.Mock()):
            impl_idl_ovn.OvsdbNbOvnIdl.ovsdb_connection = None
            self.nb_ovn_idl = impl_idl_ovn.OvsdbNbOvnIdl(self)

        self.nb_ovn_idl.idl.tables = self._tables

    def _load_nb_db(self):
        # Load Switches and Switch Ports
        fake_lswitches = TestNBImplIdlOvn.fake_set['lswitches']
        self._load_ovsdb_fake_rows(self.lswitch_table, fake_lswitches)
        fake_lsps = TestNBImplIdlOvn.fake_set['lswitch_ports']
        self._load_ovsdb_fake_rows(self.lsp_table, fake_lsps)
        # Associate switches and ports
        self._construct_ovsdb_references(
            TestNBImplIdlOvn.fake_associations['lstolsp'],
            self.lswitch_table, self.lsp_table,
            'name', 'name', 'ports')
        # Load Routers and Router Ports
        fake_lrouters = TestNBImplIdlOvn.fake_set['lrouters']
        self._load_ovsdb_fake_rows(self.lrouter_table, fake_lrouters)
        fake_lrps = TestNBImplIdlOvn.fake_set['lrouter_ports']
        self._load_ovsdb_fake_rows(self.lrp_table, fake_lrps)
        # Associate routers and router ports
        self._construct_ovsdb_references(
            TestNBImplIdlOvn.fake_associations['lrtolrp'],
            self.lrouter_table, self.lrp_table,
            'name', 'name', 'ports')
        # Load static routes
        fake_sroutes = TestNBImplIdlOvn.fake_set['static_routes']
        self._load_ovsdb_fake_rows(self.sroute_table, fake_sroutes)
        # Associate routers and static routes
        self._construct_ovsdb_references(
            TestNBImplIdlOvn.fake_associations['lrtosroute'],
            self.lrouter_table, self.sroute_table,
            'name', 'ip_prefix', 'static_routes')
        # Load acls
        fake_acls = TestNBImplIdlOvn.fake_set['acls']
        self._load_ovsdb_fake_rows(self.acl_table, fake_acls)
        # Associate switches and acls
        self._construct_ovsdb_references(
            TestNBImplIdlOvn.fake_associations['lstoacl'],
            self.lswitch_table, self.acl_table,
            'name', 'unit_test_id', 'acls')
        # Load dhcp options
        fake_dhcp_options = TestNBImplIdlOvn.fake_set['dhcp_options']
        self._load_ovsdb_fake_rows(self.dhcp_table, fake_dhcp_options)
        # Load address sets
        fake_address_sets = TestNBImplIdlOvn.fake_set['address_sets']
        self._load_ovsdb_fake_rows(self.address_set_table, fake_address_sets)

    def test_get_all_logical_switches_with_ports(self):
        # Test empty
        mapping = self.nb_ovn_idl.get_all_logical_switches_with_ports()
        self.assertItemsEqual(mapping, {})
        # Test loaded values
        self._load_nb_db()
        mapping = self.nb_ovn_idl.get_all_logical_switches_with_ports()
        expected = [{'name': utils.ovn_name('ls-id-1'),
                     'ports': ['lsp-id-11', 'lsp-id-12', 'lsp-rp-id-1']},
                    {'name': utils.ovn_name('ls-id-2'),
                     'ports': ['lsp-id-21', 'lsp-rp-id-2']},
                    {'name': utils.ovn_name('ls-id-3'),
                     'ports': ['lsp-id-31', 'lsp-id-32', 'lsp-rp-id-3',
                               'lsp-vpn-id-3']},
                    {'name': utils.ovn_name('ls-id-5'),
                     'ports': ['lsp-id-51', 'lsp-id-52', 'lsp-rp-id-5',
                               'lsp-vpn-id-5']}]
        self.assertItemsEqual(mapping, expected)

    def test_get_all_logical_routers_with_rports(self):
        # Test empty
        mapping = self.nb_ovn_idl.get_all_logical_switches_with_ports()
        self.assertItemsEqual(mapping, {})
        # Test loaded values
        self._load_nb_db()
        mapping = self.nb_ovn_idl.get_all_logical_routers_with_rports()
        expected = [{'name': 'lr-id-a',
                     'ports': {'orp-id-a1': ['10.0.1.0/24'],
                               'orp-id-a2': ['10.0.2.0/24'],
                               'orp-id-a3': ['10.0.3.0/24']},
                     'static_routes': [{'destination': '20.0.0.0/16',
                                        'nexthop': '10.0.3.253'}]},
                    {'name': 'lr-id-b',
                     'ports': {'xrp-id-b1': ['20.0.1.0/24'],
                               'orp-id-b2': ['20.0.2.0/24']},
                     'static_routes': [{'destination': '10.0.0.0/16',
                                        'nexthop': '20.0.2.253'}]},
                    {'name': 'lr-id-c', 'ports': {}, 'static_routes': []},
                    {'name': 'lr-id-d', 'ports': {}, 'static_routes': []},
                    {'name': 'lr-id-e', 'ports': {}, 'static_routes': []}]
        self.assertItemsEqual(mapping, expected)

    def test_get_acls_for_lswitches(self):
        self._load_nb_db()
        # Test neutron switches
        lswitches = ['ls-id-1', 'ls-id-2', 'ls-id-3', 'ls-id-5']
        acl_values, acl_objs, lswitch_ovsdb_dict = \
            self.nb_ovn_idl.get_acls_for_lswitches(lswitches)
        excepted_acl_values = {
            'lsp-id-11': [
                {'action': 'allow-related', 'lport': 'lsp-id-11',
                 'lswitch': 'neutron-ls-id-1',
                 'external_ids': {'neutron:lport': 'lsp-id-11'},
                 'direction': 'from-lport',
                 'match': 'inport == "lsp-id-11" && ip4'},
                {'action': 'allow-related', 'lport': 'lsp-id-11',
                 'lswitch': 'neutron-ls-id-1',
                 'external_ids': {'neutron:lport': 'lsp-id-11'},
                 'direction': 'to-lport',
                 'match': 'outport == "lsp-id-11" && ip4.src == $as_ip4_id_1'}
                ],
            'lsp-id-12': [
                {'action': 'allow-related', 'lport': 'lsp-id-12',
                 'lswitch': 'neutron-ls-id-1',
                 'external_ids': {'neutron:lport': 'lsp-id-12'},
                 'direction': 'from-lport',
                 'match': 'inport == "lsp-id-12" && ip4'},
                {'action': 'allow-related', 'lport': 'lsp-id-12',
                 'lswitch': 'neutron-ls-id-1',
                 'external_ids': {'neutron:lport': 'lsp-id-12'},
                 'direction': 'to-lport',
                 'match': 'outport == "lsp-id-12" && ip4.src == $as_ip4_id_1'}
                ],
            'lsp-id-21': [
                {'action': 'allow-related', 'lport': 'lsp-id-21',
                 'lswitch': 'neutron-ls-id-2',
                 'external_ids': {'neutron:lport': 'lsp-id-21'},
                 'direction': 'from-lport',
                 'match': 'inport == "lsp-id-21" && ip4'},
                {'action': 'allow-related', 'lport': 'lsp-id-21',
                 'lswitch': 'neutron-ls-id-2',
                 'external_ids': {'neutron:lport': 'lsp-id-21'},
                 'direction': 'to-lport',
                 'match': 'outport == "lsp-id-21" && ip4.src == $as_ip4_id_2'}
                ],
            'lsp-id-52': [
                {'action': 'allow-related', 'lport': 'lsp-id-52',
                 'lswitch': 'neutron-ls-id-5',
                 'external_ids': {'neutron:lport': 'lsp-id-52'},
                 'direction': 'from-lport',
                 'match': 'inport == "lsp-id-52" && ip4'},
                {'action': 'allow-related', 'lport': 'lsp-id-52',
                 'lswitch': 'neutron-ls-id-5',
                 'external_ids': {'neutron:lport': 'lsp-id-52'},
                 'direction': 'to-lport',
                 'match': 'outport == "lsp-id-52" && ip4.src == $as_ip4_id_5'}
                ]}
        self.assertItemsEqual(acl_values, excepted_acl_values)
        self.assertEqual(len(acl_objs), 8)
        self.assertEqual(len(lswitch_ovsdb_dict), len(lswitches))

        # Test non-neutron switches
        lswitches = ['ls-id-4']
        acl_values, acl_objs, lswitch_ovsdb_dict = \
            self.nb_ovn_idl.get_acls_for_lswitches(lswitches)
        self.assertItemsEqual(acl_values, {})
        self.assertEqual(len(acl_objs), 0)
        self.assertEqual(len(lswitch_ovsdb_dict), 0)

    def test_get_all_chassis_router_bindings(self):
        self._load_nb_db()
        bindings = self.nb_ovn_idl.get_all_chassis_router_bindings()
        expected = {'host-1': [utils.ovn_name('lr-id-a'),
                               utils.ovn_name('lr-id-b')],
                    'host-2': [utils.ovn_name('lr-id-c')],
                    ovn_const.OVN_GATEWAY_INVALID_CHASSIS: [
                        utils.ovn_name('lr-id-d')]}
        self.assertItemsEqual(bindings, expected)

        bindings = self.nb_ovn_idl.get_all_chassis_router_bindings([])
        self.assertItemsEqual(bindings, expected)

        bindings = self.nb_ovn_idl.get_all_chassis_router_bindings(['host-1'])
        expected = {'host-1': [utils.ovn_name('lr-id-a'),
                               utils.ovn_name('lr-id-b')]}
        self.assertItemsEqual(bindings, expected)

    def test_get_router_chassis_binding(self):
        self._load_nb_db()
        chassis = self.nb_ovn_idl.get_router_chassis_binding(
            utils.ovn_name('lr-id-a'))
        self.assertEqual(chassis, 'host-1')
        chassis = self.nb_ovn_idl.get_router_chassis_binding(
            utils.ovn_name('lr-id-c'))
        self.assertEqual(chassis, 'host-2')
        chassis = self.nb_ovn_idl.get_router_chassis_binding(
            utils.ovn_name('lr-id-d'))
        self.assertEqual(chassis, None)
        chassis = self.nb_ovn_idl.get_router_chassis_binding(
            utils.ovn_name('lr-id-e'))
        self.assertEqual(chassis, None)
        chassis = self.nb_ovn_idl.get_router_chassis_binding('bad')
        self.assertEqual(chassis, None)

    def test_get_unhosted_routers(self):
        self._load_nb_db()
        # Test only host-1 in the valid list
        unhosted_routers = self.nb_ovn_idl.get_unhosted_routers(['host-1'])
        expected = {utils.ovn_name('lr-id-c'): 'host-2',
                    utils.ovn_name('lr-id-d'):
                    {'chassis': ovn_const.OVN_GATEWAY_INVALID_CHASSIS}}
        self.assertItemsEqual(unhosted_routers, expected)
        # Test both host-1, host-2 in valid list
        unhosted_routers = self.nb_ovn_idl.get_unhosted_routers(['host-1',
                                                                 'host-2'])
        expected = {utils.ovn_name('lr-id-d'):
                    {'chassis': ovn_const.OVN_GATEWAY_INVALID_CHASSIS}}
        self.assertItemsEqual(unhosted_routers, expected)
        # Schedule unhosted_routers on host-2
        for unhosted_router in unhosted_routers:
            router_row = self._find_ovsdb_fake_row(self.lrouter_table,
                                                   'name', unhosted_router)
            setattr(router_row, 'options', {'chassis': 'host-2'})
        unhosted_routers = self.nb_ovn_idl.get_unhosted_routers(['host-1',
                                                                 'host-2'])
        self.assertItemsEqual(unhosted_routers, {})

    def test_get_subnet_dhcp_options(self):
        self._load_nb_db()
        subnet_options = self.nb_ovn_idl.get_subnet_dhcp_options(
            'subnet-id-10-0-2-0')
        expected_row = self._find_ovsdb_fake_row(self.dhcp_table,
                                                 'cidr', '10.0.2.0/24')
        self.assertEqual({'cidr': expected_row.cidr,
                          'external_ids': expected_row.external_ids,
                          'options': expected_row.options,
                          'uuid': expected_row.uuid},
                         subnet_options)
        subnet_options = self.nb_ovn_idl.get_subnet_dhcp_options(
            'subnet-id-11-0-2-0')
        self.assertIsNone(subnet_options)
        subnet_options = self.nb_ovn_idl.get_subnet_dhcp_options(
            'port-id-30-0-1-0')
        self.assertIsNone(subnet_options)

    def test_get_subnets_dhcp_options(self):
        self._load_nb_db()
        get_row_dict = lambda row: {
            'cidr': row.cidr,
            'external_ids': row.external_ids,
            'options': row.options,
            'uuid': row.uuid}

        subnets_options = self.nb_ovn_idl.get_subnets_dhcp_options(
            ['subnet-id-10-0-1-0', 'subnet-id-10-0-2-0'])
        expected_rows = [
            get_row_dict(
                self._find_ovsdb_fake_row(self.dhcp_table, 'cidr', cidr))
            for cidr in ('10.0.1.0/24', '10.0.2.0/24')]
        self.assertItemsEqual(expected_rows, subnets_options)

        subnets_options = self.nb_ovn_idl.get_subnets_dhcp_options(
            ['subnet-id-11-0-2-0', 'subnet-id-20-0-1-0'])
        expected_row = get_row_dict(
            self._find_ovsdb_fake_row(self.dhcp_table, 'cidr', '20.0.1.0/24'))
        self.assertItemsEqual([expected_row], subnets_options)

        subnets_options = self.nb_ovn_idl.get_subnets_dhcp_options(
            ['port-id-30-0-1-0', 'fake-not-exist'])
        self.assertEqual([], subnets_options)

    def test_get_all_dhcp_options(self):
        self._load_nb_db()
        dhcp_options = self.nb_ovn_idl.get_all_dhcp_options()
        self.assertEqual(len(dhcp_options['subnets']), 3)
        self.assertEqual(len(dhcp_options['ports_v4']), 2)

    def test_compose_dhcp_options_commands(self):
        # TODO(azbiswas): Implement in seperate patch
        pass

    def test_get_address_sets(self):
        self._load_nb_db()
        address_sets = self.nb_ovn_idl.get_address_sets()
        self.assertEqual(len(address_sets), 4)


class TestSBImplIdlOvn(TestDBImplIdlOvn):

    fake_set = {
        'chassis': [
            {'name': 'host-1', 'hostname': 'host-1.localdomain.com',
             'external_ids': {'ovn-bridge-mappings':
                              'public:br-ex,private:br-0'}},
            {'name': 'host-2', 'hostname': 'host-2.localdomain.com',
             'external_ids': {'ovn-bridge-mappings':
                              'public:br-ex'}},
            {'name': 'host-3', 'hostname': 'host-3.localdomain.com',
             'external_ids': {'ovn-bridge-mappings':
                              'public:br-ex'}},
            ]
        }

    def setUp(self):
        super(TestSBImplIdlOvn, self).setUp()

        self.chassis_table = fakes.FakeOvsdbTable.create_one_ovsdb_table()
        self._tables = {}
        self._tables['Chassis'] = self.chassis_table

        with mock.patch.object(impl_idl_ovn, 'get_connection',
                               return_value=mock.Mock()):
            impl_idl_ovn.OvsdbSbOvnIdl.ovsdb_connection = None
            self.sb_ovn_idl = impl_idl_ovn.OvsdbSbOvnIdl(self)

        self.sb_ovn_idl.idl.tables = self._tables

    def _load_sb_db(self):
        # Load Chassis
        fake_chassis = TestSBImplIdlOvn.fake_set['chassis']
        self._load_ovsdb_fake_rows(self.chassis_table, fake_chassis)

    def test_get_chassis_hostname_and_physnets(self):
        self._load_sb_db()
        mapping = self.sb_ovn_idl.get_chassis_hostname_and_physnets()
        self.assertEqual(len(mapping), 3)
        self.assertItemsEqual(mapping.keys(), ['host-1.localdomain.com',
                                               'host-2.localdomain.com',
                                               'host-3.localdomain.com'])

    def test_get_all_chassis(self):
        self._load_sb_db()
        chassis_list = self.sb_ovn_idl.get_all_chassis()
        self.assertItemsEqual(chassis_list, ['host-1', 'host-2', 'host-3'])
        # TODO(azbiswas): Unit test get_all_chassis with specific chassis
        # type