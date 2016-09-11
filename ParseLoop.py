#!/usr/local/bin/python3.5
from LoopLogic import *
from database import *
from time import sleep

def check(x):
	"""
	Checks if database has a job to do if not, then pass
	x to LoopLogic whichs a simple incremental algorithm.
	"""

	queue = Database(None).urls()

	if queue is False: 
		loop(Logic(x).do())
	
	else: main()


def loop(x):
	""" 
	Displays sleep timer and goes back to check above.
	"""

	try:
		show = '[SLEEP] %s seconds.'
		
		if x is 1:
			show=show[:-2]+'.'
		
		print(show % x)

		[ use(x) for use in [sleep,check] ]

	except KeyboardInterrupt: print('[CLOSE] %s' % now())


def main():
	""" 
	Displays current time then goes to check above.
	"""

	print('\n[CHECK] %s' % now())
	check(0)


main()
