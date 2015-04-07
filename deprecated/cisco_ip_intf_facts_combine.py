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
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib
'''
import json

FILENAME = "ip_intf_facts.json"


class FactUpdater(object):

    def __init__(self, module):
        self.ipDictHost = module.params['ipTable']
        self.hostname = module.params['hostname']
        self.fileJSON = []

    def read(self):
        try:
            with open(FILENAME, 'r') as fileObj:
                self.fileJSON = json.load(fileObj)
        except ValueError:
            # in case the file is empty create a data template
            self.fileJSON = [{}, {}]

    def write(self):
        with open(FILENAME, 'w') as fileObj:
            json.dump(self.fileJSON, fileObj, indent=4)
        return {'result': self.ipDictHost}


    def update(self):
        # get pointers to file contents
        ipDict = self.fileJSON[0]
        hostDict = self.fileJSON[1]
        ipDictUpdate = dict()
        # update second dictionary with hostname -> list of IPs
        # sorting was increase the likelihood of the first ip to be the loopback
        hostIPs = self.ipDictHost.keys()
        hostIPs.sort()
        hostDict.update({self.hostname: hostIPs})
        # update current ipDictHost to include hostname
        for ip in self.ipDictHost:
            ipDictUpdate[ip] = [self.hostname, self.ipDictHost[ip]]
        ipDict.update(ipDictUpdate)



def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            ipTable=dict(required=True, type='dict'),
            hostname=dict(required=True, type='str'),
        ),
        supports_check_mode=True,
    )
    result = ''
    # instantiate command parser
    factUpdater = FactUpdater(module)
    # read the file
    try:
        factUpdater.read()
        # update the necessary changes
        factUpdater.update()
        # write the output file
        result = factUpdater.write()
    except IOError as e:
        module.fail_json(msg="Unexpected error: " + str(e))

    module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()