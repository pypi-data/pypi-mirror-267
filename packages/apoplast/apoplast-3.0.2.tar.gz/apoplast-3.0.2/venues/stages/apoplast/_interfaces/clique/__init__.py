



from apoplast.data_nodes.clique import clique as data_nodes_clique

from apoplast._interfaces.customs.clique import clique as customs_clique
from apoplast._interfaces.sanic.clique import clique as sanic_clique

from .group import clique as clique_group
import click
import os

def run_script_from_file (
	file_path
):
	with open (file_path, 'r') as file:
		script_content = file.read()
        
	proceeds = {}	
		
	exec (script_content, {
		'__file__': os.getcwd () + "/" + file_path
	}, proceeds)
	
	variables = proceeds ['variables']
	
	print (variables)

def clique ():
	@click.group ()
	def group ():
		pass

	'''
		apoplast on --variables-path apoplast.JSON
	'''
	@click.command ("on")
	@click.option ('--variables-path', required = True)
	def on (variables_path):	
		print ("on")
		print ("variables_path:", variables_path)
		
		run_script_from_file (variables_path)
		
		
	@click.command ("off")
	def off ():	
		print ("off")
		
		

	group.add_command (on)
	group.add_command (off)
	
	
	group.add_command (clique_group ())
	
	group.add_command (data_nodes_clique ())
	group.add_command (sanic_clique ())
	group.add_command (customs_clique ())
	
	group ()




#
