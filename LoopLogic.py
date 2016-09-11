#!/usr/local/bin/python3.5
from database import *

class Logic():

	def __init__(self,x):
		self.x = x
		
	def do(self):
		"""
		Maximum sleep time of 10 is allowed.
		"""

		x = self.x
		

		if x is not 10: 
			x+=1
		
		return x
