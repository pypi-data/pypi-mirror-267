#!/usr/bin/python3

print ('regulators.proc.py')

'''
	This is called from the open
'''
import os
from os.path import dirname, join, normpath
import sys
import pathlib
def add_paths_to_python_path (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	for path in paths:
		to_add = normpath (join (this_directory, path))
		
		if (to_add not in sys.path):
			sys.path.insert (0, to_add)

#import os
print ("PYTHONPATH:", os.environ.copy () ["PYTHONPATH"])
print (sys.path)

import volts.procedures.regulators.venture.harbor as harbor

import json
import click

def clique ():
	@click.group ("regulators")
	def group ():
		pass

	'''
		./status_check regulators open --port 10000
	'''
	@group.command ("open")
	@click.option ('--port', required = True)	
	@click.option ('--details', required = True)
	def open (port, details):
		harbor.the_harbor ()


	return group
	
def clique_on ():
	print ('clique on')

	@click.group ()
	def group ():
		pass
		
	group.add_command (clique ())
	group ()

clique_on ()



#
