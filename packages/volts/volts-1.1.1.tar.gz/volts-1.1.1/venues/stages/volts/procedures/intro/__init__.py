
'''
	import pathlib
	from os.path import dirname, join, normpath
	
	this_folder = pathlib.Path (__file__).parent.resolve ()
	search = normpath (join (this_folder, "../.."))

	import volts
	volts.start (
		glob_string = search + '/**/*status.py'
	)
'''

import glob
import json
import pathlib
from os.path import dirname, join, normpath
import os		
import rich	
	
from tinydb import TinyDB, Query

import volts.topics.aggregate as aggregate
import volts.procedures.scan as scan

import volts.topics.alarm_parser as alarm_parser
import volts.topics.start.sequentially as start_sequentially
import volts.topics.start.simultaneously as start_simultaneously
import volts.topics.start.one as start_one

from volts.topics.printout.passes import printout_passes

import volts.procedures.regulators.on as regulators_on
	

'''
	
'''
def start (
	glob_string = "",
	relative_path = False,
	module_paths = [],
	
	simultaneous = False,
	simultaneous_capacity = 10,
	
	print_alarms = True,
	records = 1,
	db_directory = False,
	
	aggregation_format = 1,
	
	before = False,
	after = False
):
	#regulators_on.on ()
	#return;

	finds = glob.glob (glob_string, recursive = True)
	relative_path = str (relative_path)	
		
	if (records >= 2):
		print ()
		print ("searching for glob_string:")
		print ("	", glob_string)
		print ()
	
	if (records >= 2):
		print ()
		print ("	finds:", finds)
		print ("	finds count:", len (finds))
		print ();


	'''
		This runs the script at the "before" path,
		if the "before" path is a string.
		
		"before" is the same structure as regular checks.
	'''
	if (type (before) == str):
		before_path_statuses = start_one.now (
			before,
			module_paths,
			relative_path,
			records
		)
		print (
			"before path statuses:", 
			json.dumps (before_path_statuses, indent = 4)
		)
		
		assert (before_path_statuses ['stats']['passes'] >= 1)
		assert (before_path_statuses ['stats']['alarms'] == 0)
		

	'''
		This runs the checks either simultenously or sequentially.
	'''
	if (simultaneous == True):
		path_statuses = start_simultaneously.now (
			finds,
			module_paths,
			relative_path,
			records,
			
			simultaneous_capacity = simultaneous_capacity,
		)
	else:
		path_statuses = start_sequentially.now (
			finds,
			module_paths,
			relative_path,
			records
		)
	
	
	'''
		This runs the script at the "after" path,
		if the "after" path is a string.
		
		"after" is the same structure as regular checks.
	'''
	if (type (after) == str):
		after_path_statuses = start_one.now (
			after,
			module_paths,
			relative_path,
			records
		)
		print ("before path statuses:", json.dumps (after_path_statuses, indent = 4))
		
		assert (after_path_statuses ['stats']['passes'] >= 1)
		assert (after_path_statuses ['stats']['alarms'] == 0)


	'''
		This aggregates (or squeezes) the proceeds of the
		scan into one dictionary (JSON).
	'''
	status = aggregate.start (
		path_statuses,
		
		aggregation_format = aggregation_format
	)
	stats = status ["stats"]
	paths = status ["paths"]
	alarms = alarm_parser.start (status ["paths"])	
		
	
	
	'''
		If a db_directory is designated,
		then this adds the proceeds to the DB.
	'''
	if (type (db_directory) == str):
		os.makedirs (db_directory, exist_ok = True)
		db_file = normpath (join (db_directory, f"records.json"))
		db = TinyDB (db_file)
		
		db.insert ({
			'paths': paths, 
			'alarms': alarms,
			'stats': stats
		})
		
		db.close ()
		
	
	if (records >= 1):
		rich.print_json (data = {
			"paths": paths
		})
		
		printout_passes (paths)
		
		rich.print_json (data = {
			"alarms": alarms
		})
		rich.print_json (data = {
			"stats": stats
		})		
		
	return {
		"status": status,
		
		"paths": paths,
		"alarms": alarms,
		"stats": stats
	}
	
