#!/usr/local/bin/python3.5
from variables import *
from functions import *
from peewee import *
from brain import *
from parse import *
import datetime
import time

database = MySQLDatabase('crawl',user='root',password='secret',host='localhost')

class Card(Model):

	Set = CharField()
	Front = TextField()
	Back = TextField()
	Priority = IntegerField()
	ip = CharField()
	created_at = DateTimeField(default=now())

	class Meta:
		database = database


class Set(Model):

	Title = CharField()
	ip = CharField()
	created_at = DateTimeField(default=now())

	class Meta:
		database = database


class Trash(Model):

	Set = CharField()
	Sentence = TextField()
	ip = CharField()
	created_at = DateTimeField(default=now())

	class Meta:
		database = database


class Urls(Model):

	url = CharField()
	status = CharField()
	ip = CharField()

	class Meta:
		database = database


class Regex(Model):

	Sentence = TextField()
	Match  = TextField()
	Regex = TextField()
	Priority = IntegerField()

	class Meta:
		database = database


class Database:

	def __init__(self,sentence):

		self.sentence = sentence
		self.database = None


	def connect(self):

		database = MySQLDatabase('crawl',user='root',password='secret',host='localhost')
		database.connect()


	def close(self):

		database.close()
		self.database = None


	def urls(self):
		"""
		#1 -> Check to see if there's work to do, if there is then grab both IP
		and url.

		#2 -> Pull out only the first IP Address.

		#3 -> Pull out only the first list containing IP and URL.

		#4 -> Delete the URL that was searched from that users IP address.

		#5 -> If one or more urls were found to be worked on, then start working
		otherwise, return False to ParseLoop.py

		#6 -> Print the currently time and the string variable for start.

		#7 -> Grab the learned regular expressions from self.remember()

		#8 -> Create a variable called Data and assign it to the function data()
		under the Parse class, passing it both the grabbed URL/IP to work on and
		the learned regular expressions.

		#9 -> Pass all returned data to threads function to be added to the
		database.
		"""

		self.connect()

		#1
		check = [ [x.ip,x.url] for x in Urls.select() if x ]

		#2
		ip = ''.join([''.join(i[:1]) for i in check[:1]])

		#3
		grabbed = [ i for x in check[:1] for i in x ]

		#4
		Urls.delete().where(Urls.ip == ip).execute()

		self.close()

		#5
		if len(check) > 0:

			#6
			print(start % now(), flush=True)

			#7
			learned = self.remember()

			#8
			Data = Parse(grabbed,learned).data()

			#9
			try:
				threadsFor(Data)

			except: return

		else: return False


	def obtain(self):
		"""
		#1 -> Check if there's new regular expressions that need to be created
		from user updates.

		#2 -> If length is greater than zero, there's work to do, otherwise
		return False to BrainLoop.py

		#3 -> Pass self.memorize the information returned from brain.py which is
		passed the new material and the already known regular expressions.

		#4 -> If it fails, it's because it already has a regular expressions
		matching the one that would have been created, or because the sentence
		passed was not an accurate copy, meaning the user changed it while
		updating the card.

		#5 -> Delete the item from the database matching that sentence.
		"""

		self.connect()

		#1
		Material = [ [one.Match,one.Sentence]
		for one in Regex.select().where(Regex.Regex == "") ]

		self.close()

		#2
		if len(Material) > 0:

			#3
			try:
				self.memorize(Brain(Material,self.remember()))

			#4
			except:
				data, match, find = Material, Regex.Match, Regex.select()

				#5
				[ x.delete_instance()
				for x in find.where([(match == i[:1]) for i in data[:1]]) ]

		else: return False


	def remember(self):
		"""
		#1 -> Grab any custom regular expressions stored in the database that it
		has learned from users updating cards.
		"""

		self.connect()

		#1
		CustomList = [ z.Regex for z in Regex.select() if z.Regex is not '' ]
#		[ z.delete_instance() for z in Regex.select() ]

		return CustomList

		self.close()


	def memorize(self,x):
		"""
		#1 -> Add the regular expression it learned from brain.py to the
		database.
		"""

		self.connect()

		NewRegex = x.NewRegex
		sentence = x.sentence

		#1
		Regex.update(Regex=NewRegex).where(Regex.Sentence == sentence).execute()

		x = now(),now()

		print(out % x, flush=True)

		self.close()


	def create(self):
		"""
		#1 -> Split the list passed from parse.py into sections to be saved to
		the database.

		#2 -> Save the card to the database.

		#3 -> If there isn't already a set with a title the same as the title
		being assigned to this card, then create a new one.
		"""

		x = self.sentence

		self.connect()

		#1 Only errors out if no matches were found in Parse.py
		try:

			front = ''.join(x[0])
			back = ''.join(x[1])
			IP = ''.join(x[2])
			title = ''.join(x[3])

		except: return False, print(error1, flush=True)

		#2
		[ Card(created_at=now(),Set=title,Front=front,Back=back,Priority=0,ip=IP).save() ]

		#3
		if not Set.select().where(Set.ip == IP).where(title == Set.Title):
			[ Set(created_at=now(),Title=title,ip=IP).save() ]

		self.close()

	def collect(self):
		"""
		#1 -> Split the list apart given by parse.py into sections.

		#2 -> Save to database.
		"""

		x = self.sentence

		#1
		try:

			sentence = ''.join(x[0])
			IP = ''.join(x[1])
			title = ''.join(x[2])

		except: return False, print(error1, flush=True)

		self.connect()

		# Trash is the only table not currently being created by Laravel
#		database.create_table(Trash)

		#2
		[ Trash(created_at=now(),Set=title,Sentence=sentence,ip=IP).save() ]

		self.close()
