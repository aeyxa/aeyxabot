# aeyxabot

> **Note:** This project is intended to be used with python3.5, it uses the peewee module which requires pip3. In order to successfully install pip3 from a python install you will need to make sure to run the following command **before** the installation.

### CentOS 6 or 7 

`yum install zlib-devel bzip2-devel sqlite sqlite-devel openssl-devel`

### Ubuntu (not tested)

`apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libsqlite3-dev`

Additionally, if you're reviewing or using this package along side the laravel website aeyxa.com, make sure you have the server time set to UTC. Otherwise, Carbon may get dates incorrect due to different timezone issues.

---

## Overview
The overall purpose of the python section for this project, involves creating note cards automatically for users, who have specified a wikipedia url they wish to study.

## Logic
The overall logic behind this project is that the user submits a url, the url gets saved into a database. The url then gets searched, the content is pulled, the content is split into sentences. Then the sentences are matched against a list of regular expressions. The sentences which are matched, are split into the group that itself is matched against, and the entire sentence. The matched sentence becomes the front of the card and the back of the card is the full sentence.

---

## Example

For this example we will pretend that our user searched wikipedia.com/wiki/aeyxa and that the content on that page is:

```

This is some content on the page. 
This is a random example. 
This page contains random information regarding a random topic. 
This topic is explained in detail by the content on the page. 
This is a final sentence for the fake wikipedia page.

```

So, a web crawler goes out and fetchs the content. Then it creates a list containing each of the sentences:

```

['This is some content on the page.','This is a random example.', 'This page contains random information regarding a random topic.', 'This topic is explained in detail by the content on the page.', 'This is a final sentence for the fake wikipedia page.']

```

Now, each of these sentenced are matched against a list of regular expressions. By default the main regular expression which is checked is:

```

r'(.*?\s\b\w+ed\b.*?\s\b(by|in|on|as|is|to|the)\b\s)'

```

We check for any word at the beginning, then a word ending in [ed] then a group of common prepositions.

Any sentences that are matched, are put into a new list. In the example given above, the only sentence which would be matched in this case is the fourth sentence in the list:

```

This topic is explained in detail by the content on the page.

```

The regular expression is matched, then splits the sentence into a list containing both the full sentence in a single list.

Once more, in our example the list that would be created is:

```

['This topic is explained in?','This topic is explained in detail by the content on the page.']

```

Now this list gets saved into the database, and it is served to the user. The first part of the list (the part with the ?) is added as the front of the note card, and the full sentence is added onto the back.

If a user feels they can make the card better, they can update the card. Once the card is updated, it gets passed on to the database. Then it's cycled through and a new regular expression is created based on the change the user made and is added to the database for further use when cards get created in the future.

For example, our user gets our note card from above and decides they want to change it from:

```

"This topic is explained in?" => TO => "This topic is explained in detail by?"

```

First, a new list is created and added to the database, containing the full sentence and the new updated card front.

The list would now look like:

```

['This topic is explained in detail by?', 'This topic is explained in detail by the content on the page.']

```

Now, this gets saved in the database, and the Brain.py file is able to take this list and created a new regular expression.

The Brain.py file would take this list, and push the two parts together into one new string:

```

'This topic is explained in detail by? the content on the page.'

```

Now, this sentence is looped over against a list of regular expressions containing common prepositions. 


In this example, a new regular expression would be created for the sentence, that regular expression would come out as:

```

((\w*\s?.*?\bis\b\b\w+ed\b.*?\bis\b.*?\bby\b).*?\bthe\b.*?\bon\b.*?\bthe\b)

```


Notice how it replaces the **'?' with a ')'** allowing for only that group to be captured to be used as the front of the card in the future.

This regular expression is saved in the database and can be used right away against any new groups of text which are matched against the regular expression. The regular expression will only match if all the preposition words in the regular expression are present or more. The main benefit of this is so that the program continues to learn new regular expressions without the new expressions needing to be created by hand and added to the database.

There are other implementions that will be happening in the future for this system to become more bulletproof and match sentences with more accuracy. Such as a priority value attached to the regular expression. If five users switch the note card around in a way where two regular expressions are created, three users making one and two users making another. The one with the higher number of selections will be put at the front of the regular expression meaning it will be matched first. Until it is no longer the highest priority and then it would be pushed behind the other regular expression.


---

#PYTHON FILES							


## variables.py

Contains a random assortment of variables used throughout the project. If you run into a variable that you are unsure what it does but cannot find it in listed in the file you're in. It's likely going to be inside this file somewhere.



## functions.py

Contains functions that may be used through out the project. Currently, it contains functions related to the time module and threading.



## LoopLogic.py

Contains logic for how much the sleep timer should increment in the additional 'loop' files below.



## ParseLoop.py

Has a loop for continiously checking the database which, if there's a job to do, executes the Parse.py file.



## BrainLoop.py

Has a loop for continiously checking the database which, if there's a job to do, executes the Brain.py file.



## database.py

The file which contains all specifications and requirements for the database. The database file contains both the models for all the database tables it will be calling and the connections required to add or delete from the database.



## Parse.py

This file is passed a url which the user has searched. Once the url has been searched, it then stores that url in MySQL. MySQL serves that url through the peewee module which is called in the database.py file continiously from the ParseLoop.py file.Once the url has been found and pushed to Parse.py, the url is searched, all the content is grabbed. After the content is obtained all into one list, the list is cycled through and a list of regular expressions are matched against the sentences. Every sentence that is matched, (meaning the program understands what to do with the sentence...or thinks it does at least), is added to a new list. Then this list is cycled over and split the sentence into two groups as a list. The list contains the matched group, and the full sentence that it was matched against. Then once all the sentences are cycled through and completed, the list is returned to the database.py file.



## Brain.py

This file is used to create new regular expressions. As mentioned in the description for the Parse.py file, sentences are matched against a list of regular expressions. If a user gets a card that they believe could be better, they're able to edit that card and save the changes. Once the change is saved, and passed to the database, the BrainLoop.py file sees that there's work to be done, and calls this file.

There's many moving parts to this section, if you would like to learn more we'd recommend reviewing the file itself.




