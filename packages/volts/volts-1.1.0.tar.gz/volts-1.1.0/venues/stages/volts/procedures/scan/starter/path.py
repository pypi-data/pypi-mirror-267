

'''
	This returns the path of the "scan" process.
'''

'''
	import volts.procedures.scan.starter.path as scan_process_path
	scan_process_path.find ()
'''


import pathlib
from os.path import dirname, join, normpath


def find ():
	this_folder = pathlib.Path (__file__).parent.resolve ()
	return str (normpath (join (this_folder, "../process/scan.process.py")))