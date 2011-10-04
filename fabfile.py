from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['tukipenda@tukipenda.webfactional.com']
prompt("Enter key: ", "password") 

def production():
    """
Work on production environment
"""
    env.settings = 'production'
    env.app_folder="cbt_production"
    env.static_folder='cbt_static_production'

def staging():
    """
Work on staging environment
"""
    env.settings = 'staging'
    env.app_folder="cbt"
    env.static_folder='static_app'


def get_required_packages():
	run('cd /home/tukipenda/webapps/%s/; pip install -E VE -r CBT-Toolkit/requirements.txt' % env.app_folder)
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/lib; chmod 777 install.sh; ./install.sh' % env.app_folder)

def push():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/; git pull origin master' % env.app_folder)

def push_quick():
	local('git add .')
	local('git commit -m "quick"')
	local('git push origin master')
	push()


def set_up_binaries():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit; cp -r bin/* ~/bin/myscripts/cbt_scripts/' % env.app_folder)
	run('cd /home/tukipenda/bin/myscripts/cbt_scripts/; chmod 777 *')


def add_initial_data():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/cbt; ./script.sh load_distortions' % env.app_folder)
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/cbt; ./script.sh load' % env.app_folder)

def initialize():
	add_initial_data()
	set_up_binaries()

def check_memory():
	run('cat /home/tukipenda/logs/user/cron/cron.log | tail')
	run("ps -u tukipenda -o rss,command | sed -e '1d' | awk '{s+=$1} END {print s}'")
	run("ps -u tukipenda -o rss,command")
	
def move_static_files():
	with settings(warn_only=True):
		result=run('rm -r /home/tukipenda/webapps/%s/*' % env.static_folder)
	if result.failed and not confirm("Could not remove files.  Continue anyway?"):
		abort("Aborting at user request.")
	run('cp -r /home/tukipenda/webapps/%s/CBT-Toolkit/Media/. /home/tukipenda/webapps/%s' % (env.app_folder, env.static_folder))

def restart():
	run('/home/tukipenda/webapps/%s/apache2/bin/restart' % env.app_folder)

def stop():
	run('/home/tukipenda/webapps/%s/apache2/bin/stop' % env.app_folder)

def deploy():
	push()
	get_required_packages()
	move_static_files()
	restart()
	
def rollback():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/; git reset --hard HEAD~1' % env.app_folder)
	move_static_files()
	restart()
