

'''
	python3 --shutdown --pidfilepath /var/run/mongodb/mongod.pid
'''

'''
	import volts.procedures.portal.on as portal_on
	portal_on.on ()
'''

import multiprocessing
import subprocess
import time
import os
import atexit
import sys
import json

import volts.procedures.regulators.path as regulators_venture_path

from volts.topics.process_on import process_on

def on ():
	CWD = os.getcwd ()
	details = json.dumps ({ 
		"module_paths": sys.path 
	})
	py_proc = regulators_venture_path.discover ();
	port = 26503
	
	process_string = (
		f'''python3 "{ py_proc }" regulators open --port { port } --details \'{ details }\' '''
	)
	
	'''
	the_procedure = [
		'python3',
		f'"{ py_proc }"',
		'regulator',
		'open',
		
		'--port',
		str (port),
		
		#'--details',
		#f'"{ details }"'
	]

	print ("PYTHONPATH:", sys.path)
	print ("the_procedure:", the_procedure)
	'''

	env = os.environ.copy ()
	env ["PYTHONPATH"] = ":".join (sys.path)
	
	the_venture = process_on (
		process_string,
		CWD = CWD,
		env = env
	)
	
	#print ("the_venture:", the_venture)
	
	'''
	process = subprocess.Popen (
		the_procedure, 
		cwd = CWD,
		env = process_environment
	)
	'''
	
	
	
	pid = the_venture ["process"].pid
	
	print ("harbor pid:", pid)

	return;