# Server Provisioning

#### Set up a development environment:

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).

1. Install the [Vai](https://github.com/MatthewMi11er/vai) plugin for Vagrant with:

  `vagrant plugin install vai`

1. Copy `ansible.cfg.changeme` -> `ansible.cfg`, un-comment the line:

  `hostfile = .vagrant/inventory`

1. Copy `vars/local.yml.changeme` -> `vars/local.yml`. Put any local variable overrides in this file (or just leave it empty, if you want to use the default values). For example, to deploy from a custom branch:

  `osp_branch: feature/my-branch`

1. Start the Vagrant box with:

  `vagrant up`

1. Then, provision the box with:

  `ansible-playbook configure.yml`

  `ansible-playbook deploy.yml`

  `ansible-playbook workers.yml`

On the first run, the `deploy` playbook will take 20-30 minutes to run on most systems, since the pip install has to compile a number of very large packages (`scipy`, `pgmagick`).

#### Make a wheelhouse to speed up deployments

The slowness of the pip install is a real drag, especially when it comes time to put up a big set of 20-30 workers on EC2. To get around this, we can build a "wheelhouse" from the local Vagrant VM, which contains pre-built binaries for Ubuntu. Then, when deploying new servers (either on EC2 or locally), we can tell the provisioning scripts to use these binaries, instead of recompiling everything from scratch.

1. Log into the Vagrant box with:

  `vagrant ssh`

1. Change down into `/home/vagrant/osp`, and run:

  `pip wheel -r requirements.txt`

1. Tar up the wheelhouse:

  `tar -cvzf wheelhouse.tar.gz wheelhouse`

1. Move the tarball into the synced directory:

  `mv wheelhouse.tar.gz /vagrant`
