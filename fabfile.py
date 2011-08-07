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

def push():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/; git pull origin master' % env.app_folder)

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
	move_static_files()
	restart()
	
def rollback():
	run('cd /home/tukipenda/webapps/%s/CBT-Toolkit/; git reset --hard HEAD~1' % env.app_folder)
	move_static_files()
	restart()