# Server Provisioning

#### Set up a development environment:

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).

1. Install the [Vai](https://github.com/MatthewMi11er/vai) plugin for Vagrant with:

  `vagrant plugin install vai`

1. Symlink `config/ansible.vagrant.cfg` -> `ansible.cfg`

1. Set an environment variable called `OSP_VAGRANT` that points to a location on the local filesystem where you want the Vagrant-depolyed OSP code to by synced. Eg, in my `~/.zshrc`, I have:

  `export OSP_VAGRANT="/Users/dclure/Projects/osp-vagrant"`

  The directory doesn't need to exist - it will be automatically created when the VM is started.

1. Create a file at `~/.osp-pw.txt`, and enter the Ansible password. (Email david@dclure.org, if you don't already have it.)

1. Copy `/vars/local.changeme.yml` -> `vars/local.yml`.

1. Start the Vagrant box with:

  `vagrant up`

1. Then, provision the box with:

  `ansible-playbook configure.yml`

  `ansible-playbook deploy.yml`

  On the first run, the `deploy` playbook will take 20-30 minutes to run on most systems, since the pip install has to compile a number of very large packages (`scipy`, `pgmagick`).

1. Once the playbooks run, log into VM with:

  `vagrant ssh`

1. And start the testing Elasticsearch process:

  `sudo supervisorctl start es-test`

  (This is stopped by default, to avoid consuming resources during real extraction runs.)

1. Wait ~10s for Elasticsearch to start, and then change into `/home/vagrant/osp` and run the test suite:

  `py.test osp`

1. If this passes, the environment is fully configured and ready for work. Any changes to the code made in the synced directory (set by `OSP_VAGRANT`) will be automatically propagated to the VM, and vice versa.

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

Now, any future deployments will automatically detect the wheelhouse and deploy it to the remote server.
