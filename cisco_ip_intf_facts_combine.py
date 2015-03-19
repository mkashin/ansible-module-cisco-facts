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
module: cisco_ip_intf_facts_combine
short_description: parses and injects the results of show ip interface brief command of cisco cli
'''
EXAMPLES = '''
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib facts={{ ansible_facts }}
'''
import json

FILENAME = "ip_intf_facts.json"


class FactUpdater(object):

    def __init__(self, module):
        self.host2IP = module.params['hostTable']
        self.ip2Host = module.params['ipTable']
        self.hostname = module.params['hostname']
        self.fileObj = open(FILENAME, "r+")
        self.fileText = ''



    def read(self):
        fullFile = self.fileObj.read()
        if len(fullFile) > 0:
            self.fileText = json.loads(fullFile)

    def write(self):
        self.fileObj.write(json.dumps(self.fileText, indent=4))
        self.fileObj.close()

    def update(self):
        if len(self.fileText) > 0:
            # update ip -> host dictionary
            self.ip2Host = self.fileText[0].update(self.ip2Host)
            # update host -> ip/interface list
            self.host2IP = self.fileText[1].append(self.host2IP)
        self.fileText = [self.ip2Host, self.host2IP]



def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec = dict(
            hostTable = dict(required=True, type='list'),
            ipTable = dict(required=True, type='dict'),
            hostname = dict(required=True, type='str'),
        ),
        supports_check_mode=True,
    )

    # instantiate command parser
    factUpdater = FactUpdater(module)
    # read the file
    try:
        factUpdater.read()
        # update the necessary changes
        factUpdater.update()
        # write the output file
        factUpdater.write()
    except IOError as e:
        module.fail_json(msg="Unexpected error: " + str(e))

    module.exit_json(changed=True)

# import module snippets
from ansible.module_utils.basic import *
main()