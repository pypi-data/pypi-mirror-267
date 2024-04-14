

'''
	import volts.topics.alarm_parser as alarm_parser
'''

import json

def start (paths):
	alarms = []

	for path in paths:
		if (path ["parsed"] != True):
			alarms.append (path)

		if ("checks" not in path):
			continue;
	
		checks = path ["checks"]
	
		this_path = path ["path"]
		unsuccessful = []
		
		for check in checks:
			if (check ["passed"] == False):
				unsuccessful.append (check)
		
		if (len (unsuccessful) >= 1):
			alarms.append ({
				"path": this_path,
				"checks": unsuccessful
			})
			
	
	
	return alarms


