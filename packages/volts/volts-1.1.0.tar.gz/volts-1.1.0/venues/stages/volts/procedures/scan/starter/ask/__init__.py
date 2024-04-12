
'''
	This does up to 4 attempts with a delay of 1s in
	between each attempt.
'''

'''
	if process exits:
		{
			"path": "status_1.py",
			"empty": false,
			"parsed": true,
			"exception": true,			
			"stats": {},
			"checks": []
		}
'''


import volts.procedures.scan.starter.path as scan_process_path
import volts.procedures.scan.starter.keg as keg

import botanist.cycle.loops as cycle_loops
from botanist.cycle.presents import presents as cycle_presents

import json
import requests
from fractions import Fraction
def start_check (
	path,
	process_address,
	module_paths,
	relative_path,
	
	loops = 4,
	delay = Fraction (1, 1)
):
	def check (* positionals, ** keywords):		
		print ("attempting request", [ str (path) ])
	
		r = requests.put (
			process_address, 
			data = json.dumps ({ 
				"finds": [ str (path) ],
				"module paths": module_paths,
				"relative path": relative_path
			})
		)
		
		def format_response (TEXT):
			return json.loads (TEXT)
		
		status = format_response (r.text)

		return [ r, status ]
	
	try:
		the_proceeds = cycle_loops.start (
			check, 
			cycle_presents ([ 1 ]),
			
			loops = loops,
			delay = delay,
			
			records = 1
		)
	except Exception as E:
		print ("exception:", E)
		the_proceeds = [ None, {
			"path": str (path),
			"parsed": "unknown",
			"alarm": "An exception occurred while processing the path.",
			"exception": "A response could not be received from the capsule of the checks.  Perhaps an exit() occured."
		}]
	
	return the_proceeds;
