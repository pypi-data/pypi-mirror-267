
'''
	sanic inspect shutdown
'''

import multiprocessing
import subprocess
import time
import os
import atexit




def background (procedure, CWD):
	print ("procedure:", procedure)
	process = subprocess.Popen (procedure, cwd = CWD)


def off (
	apoplast_variables = {}
):
	print (apoplast_variables)

	harbor_path = apoplast_variables ["harbor"] ["directory"]
	process = background (
		procedure = [
			"sanic",
			"inspect",
			"shutdown"
		],
		CWD = harbor_path
	)

	return;