import random

triggers = {
	"opinion": [
		"what do you think of",
		"what do you think about",
		"what are your thoughts on",
		"what's your take on",
		"how do you feel about",
		"what's your opinion of",
		"do you like"
	]
}

aspects = {
	"creations": [
		"responsible for", # maybe remove later?
		"started",
		"oversaw",
		"initiated",
		"invented",
		"created",
		"directed"
	],
	"opinions": [
		"felt", "thought", "believed"
	],
	"attractions": [
		"liked", "loved", "appreciated", "enjoyed"
	],
	"aversions": [
		"disliked", "hated"
	]
}

values = {
	"good": [
		"charity", "peace", "whistleblow", "love",
		"goodness", "free", "liberty", "cure"
	],
	"bad": [
		"war", "death", "murder", "killing", "havoc",
		"violence", "terror", "starvation", "genocide"
	]
}

personalities = [ # ordered by intensity
	["monster", [
		"killed", "murdered", "invaded", "attacked", "terrorized", "tortured"
	]],
	["hero", [
		"saved", "rescued"
	]],
	["genius", [
		"invented", "discovered", "developed", "pioneered"
	]],
	["jerk", [
		"hurt", "harmed", "injured"
	]],
	["homie", [
		"helped", "supported", "assisted"
	]]
]

phrases = {
	"good": [
		"that rocks",
		"that's what's up",
		"heck yeah",
		"awesome"
	],
	"bad": [
		"that sucks",
		"that's lame",
		"that's wack",
		"that's rough",
		"pretty evil, right?",
		"yikes",
		":-("
	],
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
	],
	"ambivalent": [
		"eh, no strong opinion",
		"i dunno",
		"i guess i just don't know",
		"dude, i could care less"
	]
}

def randphrase(ptype, extra=None):
	if extra:
		return random.choice(phrases[ptype] + [extra])
	return random.choice(phrases[ptype])