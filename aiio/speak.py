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
	if phrase and not isinstance(phrase, str):
		print("speak.say(): deriving content")
		phrase = phrase.content()
	if not phrase:
		print("speak.say(): no phrase!")
		return
	if BRIEF and len(phrase) > 200:
		if " - " in phrase:
			[phrase, tail] = phrase.rsplit(" - ", 1)
			phrase = "%s - %s"%(truncate(phrase), tail)
		else:
			phrase = truncate(phrase)
	return phrase
#	cmd('espeak "%s"'%(phrase,))