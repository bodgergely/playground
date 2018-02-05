# http://docs.ansible.com/ansible/latest/intro_getting_started.html#
# http://docs.ansible.com/ansible/latest/intro_inventory.html

# as ubuntu
ansible all -m ping -i ./hosts/ansible_hosts --private-key ~/.ssh/aws.pem -u ubuntu
# as ubuntu, sudoing to root
ansible all -m ping -i ./hosts/ansible_hosts --private-key ~/.ssh/aws.pem -u ubuntu -b
# as ubuntu, sudoing to ubuntu
ansible all -m ping -i ./hosts/ansible_hosts --private-key ~/.ssh/aws.pem -u ubuntu --become-user ubuntu
# user specified in hosts file
ansible workers -m ping -i ./hosts/ansible_hosts --private-key ~/.ssh/aws.pem

