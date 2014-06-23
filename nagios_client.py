from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.context_managers import cd
import pwd
import os
from fabric.contrib.files import append

env.user="ubuntu"
env.use_ssh_config = True




@task
def install_nagios():
	run('sudo apt-get install -y nagios-plugins nagios-nrpe-server')


#Appends service config directives to the nagios clients
@task
def append_config_file():
	run("sudo sh -c 'echo 'allowed_hosts=127.0.0.1,10.0.2.181' >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10\" >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_load]=/usr/lib/nagios/plugins/check_load -w 15,10,5 -c 30,25,20\" >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10%\" >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_zombie_procs]=/usr/lib/nagios/plugins/check_procs -w 5 -c 10 -s Z\" >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_total_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200\" >> /etc/nagios/nrpe_local.cfg'")
	run("sudo sh -c 'echo \"command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 50% -c 25%\" >> /etc/nagios/nrpe_local.cfg'")

def restart_nagios():
	run('sudo service nagios-nrpe-server restart')

@task
def deploy():
	install_nagios()
	append_config_file()
	restart_nagios()



#Run this command with ex:"fab -f nagios_client.py test --hosts=apl-monitor"
@task
def test():
	get_hostname()
