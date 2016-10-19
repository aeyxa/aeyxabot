#!/usr/local/bin/python3.5
import datetime
import re

# This section is used for create note cards

right = datetime.datetime
hms = "%Y-%m-%d %H:%M:%S"
each = '%s\n%s %s'

strip = re.compile

Custom = r'(.*\s\bshould\b\s\bbe\b\s\ba\b\s.*?\bfor\b\s)'

Default = r'(.*?\s\b\w+ed\b.*?\s\b(by|in|on|as|is|to|the)\b\s)'

ForRegexIn = r'(^(?!It).*?\s((\w+ed.*?\s\b(by|in|on|as|is|to|the)\b\s)|(consists\sof)\s))'

unwanted = r"(\[\d+\])|(\[update\])|(\[citation needed\])|(b\'|b\")"
spaces = r'[.]\s(?=[A-Z])'
replace = r'(.*[.]\n)'
nl = '.\n'

reset = '[RESET] %s'
start = '\n[START] %s'
fatal = "[FATAL]"
error1 = '[ERROR] Insufficient data passed from Parser.'
error2 = '[ERROR] Syntax error for string:\n%s'
saved = '[SAVED] %s'
out = '[SAVED] %s\n[RESET] %s'

"""

	#######################################################################

		This section below is used for creating new regular expressions

	#######################################################################

"""

RegexSpecial = r'(\?)'

force = ''
space = ' '
FixString = r'(\)\()'
Replace = r'(\\\?)'
#firstWord = r'(\w*\s?)'
firstWord = r'((\w*\s?)'

# RegexSpecial must be the last variable in Knowledge.

Knowledge = [r'(\"\w)',r'(\w\")',r'(\b\w+ed\b)',r'(\ba\b)',r'(\ban\b)',r'(\baboard\b)',r'(\babout\b)',r'(\babove\b)',r'(\bacross\b)',r'(\bafter\b)',r'(\bagainst\b)',r'(\balong\b)',r'(\bamid\b)',r'(\bamong\b)',r'(\banti\b)',r'(\baround\b)',r'(\bas\b)',r'(\bat\b)',r'(\bbefore\b)',r'(\bbehind\b)',r'(\bbelow\b)',r'(\bbeneath\b)',r'(\bbeside\b)',r'(\bbesides\b)',r'(\bbetween\b)',r'(\bbeyond\b)',r'(\bbut\b)',r'(\bby\b)',r'(\bconcerning\b)',r'(\bconsidering\b)',r'(\bdespite\b)',r'(\bdown\b)',r'(\bduring\b)',r'(\bexcept\b)',r'(\bexcepting\b)',r'(\bexcluding\b)',r'(\bfollowing\b)',r'(\bfor\b)',r'(\bfrom\b)',r'(\bin\b)',r'(\bis\b)',r'(\binside\b)',r'(\binto\b)',r'(\blike\b)',r'(\bminus\b)',r'(\bnear\b)',r'(\bof\b)',r'(\boff\b)',r'(\bon\b)',r'(\bonto\b)',r'(\bopposite\b)',r'(\boutside\b)',r'(\bover\b)',r'(\bpast\b)',r'(\bper\b)',r'(\bplus\b)',r'(\bregarding\b)',r'(\bround\b)',r'(\bsave\b)',r'(\bsince\b)',r'(\bthan\b)',r'(\bthe\b)',r'(\bthrough\b)',r'(\bto\b)',r'(\btoward\b)',r'(\btowards\b)',r'(\bunder\b)',r'(\bunderneath\b)',r'(\bunlike\b)',r'(\buntil\b)',r'(\bup\b)',r'(\bupon\b)',r'(\bversus\b)',r'(\bvia\b)',r'(\bwith\b)',r'(\bwithin\b)',r'(\bwithout\b)',RegexSpecial]
