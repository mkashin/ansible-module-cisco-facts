
#./cisco_fact_gathering ip=172.16.0.1 username=admin password=12345
dos2unix cisco_ip_intf_facts.py
cp cisco_ip_intf_facts.py library/
ansible-playbook cisco_fact_gathering.yml -v

