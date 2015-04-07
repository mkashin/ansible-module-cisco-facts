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
module: cisco_scenarios
short_description: parses the results of traceroute command of cisco cli
'''
EXAMPLES = '''
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib
'''
import os

FOLDER = "./scenarios/"
PREFIX = "scenario-"

def read_scenario(scenario):
    filename = FOLDER + scenario
    ref_scenario = dict()
    with open(filename, 'r') as fileObj:
        for line in fileObj:
            if not line.startswith('#') and len(line) > 5:
                seqN, fromDev, toDev, viaDev = line.split()
                to_dict = {toDev: [
                    viaDev, seqN
                ]}
                if fromDev in ref_scenario:
                    ref_scenario[fromDev].update(to_dict)
                else:
                    ref_scenario.update({
                        fromDev: to_dict
                    })
    return ref_scenario


def write_scenario(text, filename):
    json_filename = FOLDER + filename.split('.')[0] + '.json'
    with open(json_filename, 'w') as fileObj:
            json.dump(text, fileObj, indent=4)


def convert():
    for scenario in os.listdir(FOLDER):
        if scenario.startswith('scenario') and scenario.endswith('.txt'):
            write_scenario(read_scenario(scenario), scenario)


def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict( ),
        supports_check_mode=True,
    )
    convert()
    module.exit_json(changed=False)

# import module snippets
from ansible.module_utils.basic import *
main()