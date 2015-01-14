## OSP worker provisioning

To provision a Vagrant VM:

1. Run `vagrant up`, which will mount the VM and apply the `site.yml` playbook.

1. Symlink `./config/ansible.cfg.vagrant` -> `./ansible.cfg`.

1. Then, playbooks can be run without any extra flags. Eg, `ansible-playbook deploy.yml`.

To provision an EC2 instance:

1. Symlink `./config/ansible.cfg.ec2` -> `./ansible.cfg`.

1. Symlink `./config/hosts.ec2` -> `./hosts` and define targets in the file.

1. Run playbooks normally with `ansible-playbook site.yml`, etc.
