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
module: cisco_trace_compare
short_description: parses the results of traceroute command of cisco cli
'''
EXAMPLES = '''
- cisco_ip_intf_facts: text={{ text_inventory.stdout }} command=siib
'''


class ResultCompare(object):

    def __init__(self, module):
        self.dest_host = module.params['dest_host']
        self.src_host = module.params['src_host']
        self.trace_path = module.params['trace_path'][self.dest_host]
        self.ref_scenario = module.params['scenario']
        self.ip_host = module.params['ip_host']
        self.scenario_file = module.params['scenario_file']

    def log(self, error):
        filename = './scenarios/err-' + self.scenario_file
        with open(filename, 'a') as fileObj:
            fileObj.write(error)

    def compare(self):
        trace_path_new = list()
        for dev in self.trace_path:
            trace_path_new.append(self.ip_host[dev][0])
        #print "from !!!" + str(self.src_host)
        #print "dest !!!" + str(self.dest_host)
        #print "ref_scenario !!!" + str(self.ref_scenario)
        #print "trace !!!" + str(self.trace_path)
        #print "trace_new !!!" + str(trace_path_new)
        if self.src_host in self.ref_scenario:
            if self.dest_host in self.ref_scenario[self.src_host]:
                ref_path, seq = self.ref_scenario[self.src_host][self.dest_host]
                if ref_path not in trace_path_new:
                    msg = "Failed scenario " + seq + ". Traceroute from " + self.src_host + " to " + self.dest_host + " has not traversed " + ref_path
                    msg += "\r\n Actual path taken: " + ' -> '.join([self.src_host] + trace_path_new) + "\r\n"
                    return 1, msg
        return 0, 'no error'


def main():
    # creating module instance. accepting raw text output and abbreviation of command
    module = AnsibleModule(
        argument_spec=dict(
            dest_host=dict(required=True, type='str'),
            src_host=dict(required=True, type='str'),
            trace_path=dict(required=True, type='dict'),
            scenario=dict(required=True, type='dict'),
            ip_host=dict(required=True, type='dict'),
            scenario_file=dict(required=True, type='str')
        ),
        supports_check_mode=True,
    )

    # instantiate command parser
    comparator = ResultCompare(module)
    # parse the output of show ip interface brief command
    rc, error = comparator.compare()
    # exiting module
    if rc != 0:
        comparator.log(error)
        module.exit_json(changed=True)
    else:
        module.exit_json(changed=False)

# import module snippets
from ansible.module_utils.basic import *
main()