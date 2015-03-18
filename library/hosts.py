#!/usr/bin/python
import json

myInventory = {
 "_meta": {
   "hostvars": {
     "HomeRouter": { "ansible_ssh_host": "172.16.0.1" },
     "IOU": { "ansible_ssh_host": "172.16.0.254" }
   }
 },
 "cisco-devices": [
   "HomeRouter",
   "IOU"
 ]
}
print json.dumps(myInventory)

