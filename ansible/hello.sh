# http://docs.ansible.com/ansible/latest/intro_getting_started.html#
# http://docs.ansible.com/ansible/latest/intro_inventory.html
ansible all -a "/bin/echo hello" -i ./hosts/ansible_hosts --private-key ~/.ssh/aws.pem -u ubuntu

