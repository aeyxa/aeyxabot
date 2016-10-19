#!/usr/local/bin/python3.5
from variables import *
from peewee import *
import threading
import datetime
import time
import re

class Brain:

	def __init__(self,Material,memory):
		"""This data comes from database.py"""

		self.Material = Material
		self.memory = memory
		self.sort()


	def sort(self):
		"""
		#1 -> Check if there's more than one new regular expression that needs to be created
			from the database query. If there is more than one, then split off the first one
			and pass it to study. If there is only one then pass it to study, don't split it.
		"""

		#1
		if len(self.Material) > 1:
			split = [ one for each in self.Material[:1] for one in each]
			self.study(split)
		else:
			split = [ one for each in self.Material for one in each ]
			self.study(split)


	def study(self,material):
		"""
		#2 -> Create a variable called match which is equal to the string from the front of
			the card updated by the user. Then, match that variable against the back of the
			card which held the entire sentence. Create a new variable which has merged the
			two front and back together.

			match  ->  This is a?
			one    ->  This is a very important sentence.
			x      ->  This is a? very important sentence.
		"""

		#2
		match = ''.join(material[:1])

		concept = [ x for one in material[1:2] for x in [re.sub(match, match, one)] ]

		self.learn(''.join(concept),''.join(material[1:2]))


	def learn(self,concept,sentence):
		"""
		#3 -> Search through each in Knowledge make a list of each regex match in the sentence.

		#4 -> Insert a regular expression with double parenthesis at the start of the regular
			expression created in #3. This is so that we can use the .group(1) on the regular
			expression to only obtain the part we expect to place a ? on.

		#5 -> Since the regular expression list is grouped together in parenthesis, we can find
			the beginning and end of each match by searching for )( and replacing them with .*?
			to allow for any non matched words to be accepted. Now, as mentioned before in step
			#4, we added (( to be able to .group(1). So, now we need to be able to complete the
			parenthesis by replacing the special regex '\\\?' with a ). Meaning it will capture
			any words till the ? originally given when the user submitted an update to the card.
		"""

		#3
		MatchList = [ x for word in concept.split() for x in Knowledge if re.search(x,word)]

		#4
		MatchList.insert(0,r'((\w*\s?)')
		MatchList = ''.join(MatchList)

		#5
		NewRegex = re.sub(r'(\)\()','.*?',MatchList)
		NewRegex = re.sub(r'([.]\*\?\\\?)',')',NewRegex)

		self.validate(NewRegex,sentence)


	def validate(self,NewRegex,sentence):
		"""
		#6 -> Validate that the regular expression created matched the sentence that was passed
			because otherwise invalidate regular expressions may be created. An example of this
			would be if a user completely changes the input to something that doesn't match any
			words in the sentence. Then, nothing will be saved in a way that can be read by the
			database file. If a match is made then self.NewRegex = NewRegex allows the database
			file to read the sentence which will not throw an error, which will allow the regex
			to be saved in the database.

			Additionally, we are checking to make sure that the regular expression has not been
			already saved in the database. If there's nothing in the database, (such as after a
			rollback), then just allow it to be created.
		"""

		#6
		if re.search(NewRegex,sentence):
			if len(self.memory) > 0:
				for x in self.memory:
					if x != NewRegex:
						self.NewRegex = NewRegex
						self.sentence = sentence
			else:
				self.NewRegex = NewRegex
				self.sentence = sentence

		else: return
