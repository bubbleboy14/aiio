import re
#from cantools.util import cmd

BRIEF = False
NPRX = re.compile(r'\([^)]*\)')
def setBrevity(onoroff):
	global BRIEF
	BRIEF = onoroff

def noParens(phrase):
	return re.sub(NPRX, "", phrase)

def truncate(phrase):
	print("[IN]", phrase)
	phrase = noParens(phrase)
	for punct in ["!", "?", ".", ";", ":"]:
		if len(phrase) > 200: # leaves room for comfortable split
			phrase = phrase[:300].rsplit(punct, 1)[0]
	print("[OUT]", phrase)
	return phrase

def say(phrase):
	if BRIEF and len(phrase) > 200:
		phrase = truncate(phrase)
	return phrase
#	cmd('espeak "%s"'%(phrase,))