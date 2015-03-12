#!/usr/bin/python
import json

myInventory = {
 "_meta": {
   "hostvars": {
     "HomeRouter": { "ansible_ssh_host": "172.16.0.1" }
   }
 },
 "cisco-devices": [
   "HomeRouter"
 ]
}
print json.dumps(myInventory)

