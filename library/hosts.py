#!/usr/bin/python
import json

myInventory = {
 "_meta": {
   "hostvars": {
     "R1": { "ansible_ssh_host": "10.0.0.1" },
     "R2": { "ansible_ssh_host": "10.0.0.2" },
     "R3": { "ansible_ssh_host": "10.0.0.3" },
     "R4": { "ansible_ssh_host": "10.0.0.4" },
     "localhost": { "ansible_ssh_host": "127.0.0.1" }
   }
 },
 "cisco-devices": [
   "R1",
   "R2",
   "R3",
   "R4"
 ],
 "localhost": [
   "localhost"
 ]
}
print json.dumps(myInventory)

