
#./cisco_fact_gathering ip=172.16.0.1 username=admin password=12345
dos2unix *.py
cp *.py library/
ansible-playbook cisco_fact_gathering.yml -v

