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

FILENAME = "ip_intf.facts"

class FactUpdater(object):

	def __init__(self, hostTable, ipTable):

        self.host2IP = self.module.params['hostTable']
        self.ip2Host = self.module.params['ipTable']
        self.hostname = self.module.params['hostname']
        self.fileObj = open (FILENAME, "r+") 
        self.fileText = ''

    def read(self):
        self.fileText=self.fileObj.read().replace('\n', '')

    def write(self):
        self.fileObj.write(self.fileText)

	def update(self):

         self.host2IP = ''.join(self.host2IP)

         return 0,result

def main():
	# creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec = dict(
            hostTable = dict(required=True, type='dict'),
            ipTable = dict(required=True, type='list'),
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
    except:
        module.fail_json(msg="Unexpected error: " + sys.exc_info()[0])

   	module.exit_json(changed=True)

# import module snippets
from ansible.module_utils.basic import *
main()