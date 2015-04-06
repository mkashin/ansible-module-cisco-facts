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
module: cisco_read_facts
short_description: descriptopm
'''
EXAMPLES = '''
- example
'''
import json

FILENAME = "ip_intf_facts.json"


class Reader():

    def __init__(self):
        self.JSON = [{}, {}]

    def read(self):
        with open(FILENAME, 'r') as fileObj:
            self.JSON = json.load(fileObj)

        return self.JSON[0]


def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
    #        ipTable=dict(required=True, type='dict'),
    #        hostname=dict(required=True, type='str'),
        )
    )
    result = ''
    # instantiate command parser
    reader = Reader()
    # read the file
    try:
        result = reader.read()
    except IOError as e:
        module.fail_json(msg="Unexpected error: " + str(e))

    module.exit_json(changed=False, ansible_facts=result)

# import module snippets
from ansible.module_utils.basic import *
main()