



'''
	import volts.procedures.portal.path as portal_venture_path
	portal_venture_path.discover ()
'''
import pathlib
from os.path import dirname, join, normpath

def discover ():
	return str (
		normpath (join (
			pathlib.Path (__file__).parent.resolve (), 
			"venture/regulators.proc.py"
		))
	)