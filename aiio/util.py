import random

phrases = {
	"greeting": [
		"salutations,",
		"hello",
		"hi",
		"nice to meet you",
		"greetings",
		"what's up",
		"what's shakin"
	],
	"rephrase": [
		"so you're telling me that",
		"in other words,",
		"so,",
		"ok, so",
		"you're basically saying that"
	],
	"inquire": [
		"please elaborate on",
		"tell me more regarding",
		"i'd like to know more about"
	],
	"noted": [
		"noted",
		"thanks for the info",
		"cool",
		"ok, great"
	],
	"what": [
		"what?",
		"i'm not sure what you mean",
		"i don't get it"
	],
	"unsure": [
		"i'm not sure",
		"it's hard to say",
		"ummm.."
	],
	"exhausted": [
		"how am i supposed to know?",
		"i don't know anymore :(",
		"you tell me"
	],
	"agree": [
		"exactly!",
		"i completely agree.",
		"you're preaching to the choir :)",
		"you've got my vote!"
	],
	"disagree": [
		"i don't think you're right.",
		"you're wrong!",
		"not exactly...",
		"don't say that.",
		"i don't want to hear it!"
	]
}

def randphrase(ptype, extra=None):
	if extra:
		return random.choice(phrases[ptype] + [extra])
	return random.choice(phrases[ptype])