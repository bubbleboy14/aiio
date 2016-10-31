from cantools.util import cmd

BRIEF = False
def setBrevity(onoroff):
	global BRIEF
	BRIEF = onoroff

def say(phrase):
	print "[IN]", phrase
	if BRIEF and len(phrase) > 500:
		phrase = phrase[:500].rsplit(".", 1)[0]
		print "[OUT]", phrase
	return phrase
#	cmd('espeak "%s"'%(phrase,))