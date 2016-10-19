#!/usr/local/bin/python3.5
from urllib.request import urlopen
from bs4 import BeautifulSoup
from functions import *
from variables import *
from database import *
from peewee import *
import threading
import time
import re

class Parse:

    def __init__(self,url,custom):
        """ These come from database.py """
        self.ip = ''.join(url[:1])
        self.url = ''.join(url[1:2])
        self.custom = custom


    def data(self):
        """
        Open url passed from database, if unable to, display error of invalid url. Then once the url
        has been opened, grab all the paragraph tags and strip it into only the text. Remove all the
        unwanted wikipedia information then split each sentence into it's own line to make it easier
        to read through each one in parse().
        """

        try:
            page = BeautifulSoup(urlopen(self.url), "html.parser")

        except:
            print('[ERROR] Invalid URL')
            return False


        Content = [ text.get_text() for text in page.findAll('p') ]
        self.title = ''.join([ title.get_text() for title in page.findAll('h1')])
        text = [ re.sub(unwanted,'',each) for each in Content ]
        self.Sentences = [ re.findall(replace, re.sub(spaces,nl,each)) for each in text ]

        return self.parse()


    def parse(self):
        """
        Cycle through each sentence, for each sentence cycle through each in regular expression list
        match the list against the sentence. If a match is found, create a new variable called x and
        find the regular expression match in the sentence. Then create a new list which contains the
        match and the full sentence.

        Example -> 'The best random example ever created by any human in existance.'

        Outputs -> [
                      'The best random example ever created by?',
                      'The best random example ever created by any human in existance.'
                   ]
        """


        RegexList, Content = push(self.custom,[Default]), push(self.Sentences)

        self.Find =	[
                        [x.group(1).strip()+'?',i,self.ip,self.title]
                        for i in Content for regex in RegexList
                        if re.compile(regex).match(i)
                        for x in [re.search(regex,i)]
                    ]

        return self.recycle()


    def recycle(self):
        """
        #1 -> Create a list of the full sentences for each in self.Find

        #2 -> Create a new list for each in self.Sentences if not in #1

        #3 -> Create a new list of both the found sentences and ones that
            are not found, then return them to database.py.
        """

        #1
        Found = [ x[1] for x in self.Find ]

        #2
        discard = [ [i,self.ip,self.title] for i in push(self.Sentences) if i not in Found ]

        #3
        Paired = [ self.Find,discard ]

        return Paired
