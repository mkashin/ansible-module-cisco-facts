#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2015, Michael Kashin <m.kashin84@gmail.com>
#
# This file is part of Ansible
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
module: cisco_ip_intf_facts
short_description: parses and injects the results of show ip interface brief command of cisco cli
'''
EXAMPLES = '''
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib facts={{ ansible_facts }}
'''


class SIIBparse(object):

    def __init__(self, module):
        self.module = module

    def parse(self):
        ipDict = dict()
        # go through each line of text looking for interface in 'up' state
        for line in self.module.params['text'].split("\n"):
            row = line.split()
            if len(row) > 0 and row[-1] == 'up':
                ipAddress = row[1]
                intfName = row[0]
                ipDict[ipAddress] = intfName
        result = {
            "IPs": ipDict
        }

        return 0, result


def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            text=dict(required=True, type='str')
        ),
        supports_check_mode=True,
    )

    # instantiate command parser
    siib = SIIBparse(module)
    # parse the output of show ip interface brief command
    rc, result = siib.parse()
    # exiting module
    if rc != 0:
        module.fail_json(msg="Failed to parse. Incorrect input.")
    else:
        module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()