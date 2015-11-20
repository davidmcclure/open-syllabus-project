# Server Provisioning

### Set up a development environment:

- Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).

- Install the [Vai](https://github.com/MatthewMi11er/vai) plugin for Vagrant with:

  `vagrant plugin install vai`

- Copy `ansible.cfg.changeme` -> `ansible.cfg`, un-comment the line:

  `hostfile = .vagrant/inventory`

- Copy `vars/local.yml.changeme` -> `vars/local.yml`. Put any local variable overrides in this file (or just leave it empty, if you want to use the default values). For example, to deploy from a custom branch, just set the new value:

  `osp_branch: feature/my-branch`
