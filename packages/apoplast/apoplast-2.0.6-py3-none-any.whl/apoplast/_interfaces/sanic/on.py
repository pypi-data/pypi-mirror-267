

'''
	python3 --shutdown --pidfilepath /var/run/mongodb/mongod.pid
'''

import multiprocessing
import subprocess
import time
import os
import atexit

def background (procedure, CWD):
	print ("procedure:", procedure)

	process = subprocess.Popen (procedure, cwd = CWD)
	pid = process.pid
	
	print ("sanic pid:", pid)

def on (
	apoplast_variables = {}
):
	print (apoplast_variables)

	harbor_path = apoplast_variables ["harbor"] ["directory"]
	
	process = background (
		procedure = [
			"sanic",
			f'harbor:create',
			f'--port=8000',
			f'--host=0.0.0.0',
			'--fast',
			'--factory'
		],
		CWD = harbor_path
	)

	return;