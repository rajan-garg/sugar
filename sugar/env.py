import os
import sys
import pwd

try:
	from sugar.__uninstalled__ import *
except ImportError:
	from sugar.__installed__ import *

import sugar.setup
import sugar.conf

def add_to_python_path(path):
	sys.path.insert(0, path)
	if os.environ.has_key('PYTHONPATH'):
		old_path = os.environ['PYTHONPATH']
		os.environ['PYTHONPATH'] = path + ':' + old_path 
	else:
		os.environ['PYTHONPATH'] = path

def add_to_bin_path(path):
	if os.environ.has_key('PATH'):
		old_path = os.environ['PATH']
		os.environ['PATH'] = path + ':' + old_path
	else:
		os.environ['PATH'] = path

def setup():
	for path in sugar_python_path:
		add_to_python_path(path)

	for path in sugar_bin_path:
		add_to_bin_path(path)

	if sugar_source_dir:
		source = os.path.join(sugar_source_dir, 'activities')
		runner = os.path.join(sugar_source_dir, 'shell/sugar-activity-factory')
		sugar.setup.setup_activities(source, get_activities_dir(), runner)
		
		bin = os.path.join(sugar_source_dir, 'shell/sugar-presence-service')
		sugar.setup.write_service('org.laptop.Presence', bin,
								  get_services_dir())

	registry = sugar.conf.get_activity_registry()
	registry.scan_directory(get_activities_dir())

	read_profile()

def read_profile():
	profile = sugar.conf.get_profile()
	profile.set_path(get_profile_path())
	profile.read()

def get_profile_path():
	if os.environ.has_key('SUGAR_PROFILE'):
		profile_id = os.environ['SUGAR_PROFILE']
	else:
		profile_id = 'default'
	path = os.path.expanduser('~/.sugar')

	return os.path.join(path, profile_id)

def get_nick_name():
	profile = sugar.conf.get_profile()
	return profile.get_nick_name()

def get_data_dir():
	return sugar_data_dir

def get_dbus_config():
	return sugar_dbus_config

def get_data_file(filename):
	return os.path.join(get_data_dir(), filename)
		
def get_activities_dir():
	return sugar_activities_dir

def get_services_dir():
	return sugar_activities_dir
