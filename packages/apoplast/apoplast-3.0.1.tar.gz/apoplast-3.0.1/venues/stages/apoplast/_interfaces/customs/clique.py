


import apoplast._interfaces.customs.on as customs_on
import apoplast._interfaces.customs.off as customs_off
import apoplast._interfaces.customs.status as customs_status

	
import click
import time

def clique ():

	@click.group ("customs")
	def group ():
		pass

	@group.command ("on")
	#@click.option ('--example-option', required = True)
	def on ():
		print ("on")
		customs_on.on ()
		
		time.sleep (1)
		

	@group.command ("off")
	#@click.option ('--example-option', required = True)
	def off ():
		print ("off")
		customs_off.off ()

		
		time.sleep (1)
		
		
	@group.command ("status")
	#@click.option ('--example-option', required = True)
	def on ():
		print ("on")
		customs_status.status ()


	return group




#



