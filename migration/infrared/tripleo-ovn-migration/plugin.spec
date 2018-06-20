---
config:
    plugin_type: install
subparsers:
    tripleo-ovn-migration:
        description: Migrate an existing TripleO overcloud from Neutron ML2OVS plugin to OVN
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: Containers
              options:
                  registry-namespace:
                      type: Value
                      help: The alternative docker registry namespace to use for deployment.

                  registry-prefix:
                      type: Value
                      help: The images prefix

                  registry-tag:
                      type: Value
                      help: The images tag

                  registry-mirror:
                      type: Value
                      help: The alternative docker registry to use for deployment.

            - title: Deployment Description
              options:
                  version:
                      type: Value
                      help: |
                          The product version
                          Numbers are for OSP releases
                          Names are for RDO releases
                          If not given, same version of the undercloud will be used
                      choices:
                        - "7"
                        - "8"
                        - "9"
                        - "10"
                        - "11"
                        - "12"
                        - "13"
                        - "14"
                        - kilo
                        - liberty
                        - mitaka
                        - newton
                        - ocata
                        - pike
                        - queens
                        - rocky
                  install_from_package:
                      type: Bool
                      help: Install python-networking-ovn-migration-tool rpm
                      default: True
