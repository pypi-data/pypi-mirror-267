



import apoplast._interfaces.sanic.on as sanic_on
import apoplast._interfaces.sanic.off as sanic_off

from apoplast._variables import prepare_variables
	
import click
import time

def clique ():

	@click.group ("sanic")
	def group ():
		pass

	@group.command ("on")
	#@click.option ('--example-option', required = True)
	def on ():
		print ("on")
		sanic_on.on (
			apoplast_variables = prepare_variables ({})
		)
		
		time.sleep (1)
		

	@group.command ("off")
	#@click.option ('--example-option', required = True)
	def off ():
		print ("off")
		sanic_off.off (
			apoplast_variables = prepare_variables ({})
		)
		
		time.sleep (1)
		
		
	@group.command ("status")
	#@click.option ('--example-option', required = True)
	def on ():
		print ("on")
		sanic_status.status (
			apoplast_variables = prepare_variables ({})
		)
		
		time.sleep (1)

	return group




#



