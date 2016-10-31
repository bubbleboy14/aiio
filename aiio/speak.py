import re
from cantools.util import cmd

BRIEF = False
NPRX = re.compile(r'\([^)]*\)')
def setBrevity(onoroff):
	global BRIEF
	BRIEF = onoroff

def noParens(phrase):
	return re.sub(NPRX, "", phrase)

def say(phrase):
	print "[IN]", phrase
	if BRIEF and len(phrase) > 200:
		phrase = noParens(phrase)
		if (len(phrase)) > 200:
			phrase = phrase[:200].rsplit(".", 1)[0]
		print "[OUT]", phrase
	return phrase
#	cmd('espeak "%s"'%(phrase,))