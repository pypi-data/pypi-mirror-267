
'''
	python3 /apoplast/venues/stages/apoplast/_interfaces/sanic/__init__.py
	
	sanic /apoplast/venues/stages/apoplast/_interfaces/sanic
'''

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''

def add_paths_to_system (paths):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))

add_paths_to_system ([
	'../../../../stages',
	'../../../../stages_pip'
])

'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	--factory
'''

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	from sanic import Sanic
	from sanic.response import text

	app = Sanic (__name__)
	app.config.INSPECTOR = True

	# Define a route
	@app.route ("/")
	async def hello (request):
		return text ("Hello, Sanic!")
		
	return app

'''
from apoplast._variables import prepare_variables


def main ():
	apoplast_variables = prepare_variables ({
		"moon": {}
	})

	# Create a Sanic app
	app = Sanic(__name__)

	# Define a route
	@app.route("/")
	async def hello(request):
		return text("Hello, Sanic!")

	return [ app, apoplast_variables ["harbor"] ["PID_path"] ]
'''

'''
if __name__ == "__main__":
	[ app, pid_file ] = main ()
	app.run (host = "0.0.0.0", port = 8000)
'''