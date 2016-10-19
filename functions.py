#!/usr/local/bin/python3.5
from variables import *
import database
import threading
import datetime


def now():
    """
    Full time and date displayed here except milliseconds.
    """

    return datetime.datetime.now().strftime(hms)

def hour():
    """
    Only the current hour is displayed here, this is used
    in the logic loop to determine the maximum sleep time.
    """

    return int(datetime.datetime.now().strftime("%H"))

def current():
    """
    Displays the current time without the date.
    """

    return date.time.datetime.now().strtime("%H:%M:%S")

def threadsFor(Work):
    """
    This section is used for creating threads for each
    sentence that needs to be added to the database in
    the Parse.py file which is called from database.py.

    'keep' are the matched sentences, those go to the create() in the
    database.py file.

    'toss' are the unmatched sentences, those go to the collect() in the
    database.py file.
    """

    keep = Work[0]
    toss = Work[1]

    Threads = []

    for job in keep:
        execute = database.Database(job)
        thread = threading.Thread(target=execute.create())
        Threads.append(thread)
        thread.start()

        [ thread.join() for thread in Threads ]

    for job in toss:
        execute = database.Database(job)
        thread = threading.Thread(target=execute.collect())
        Threads.append(thread)
        thread.start()

        [ thread.join() for thread in Threads ]

    print(reset % now(), flush=True)


def push(Passed,*args):
    """
    Adds the contents of one list to another list.
    """
    if len(args) is 0:
        predefined = []
        for z in Passed:
            predefined.extend(z)
        return predefined

    elif len(args) is 1:
        [ Passed.extend(z) for z in args ]
        return Passed

    else: return None
