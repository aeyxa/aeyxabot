#!/usr/local/bin/python3.5
from database import *
from LoopLogic import *
from time import sleep
import threading


def check(x):
	"""
	Checks if database has a job to do if not, then pass
	x to LoopLogic whichs a simple incremental algorithm.
	"""

	queue = Database(None).obtain()

	if queue is False:
		loop(Logic(x).do())

	else: main()


def loop(x):
	"""
	Displays sleep timer and goes back to check above.
	"""

	try:

		[ use(x) for use in [sleep,check] ]

	except KeyboardInterrupt: print('\n[BRAIN]\n[CLOSE] %s' % now(), flush=True)


def main():
	"""
	Displays current time then goes to check above.
	"""

	print('\n[BRAIN]\n[CHECK] %s' % now(), flush=True)

	check(0)


main()
