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
		"murdered", "invaded", "terrorized", "tortured"
	]],
	["psycho", [
		"misled", "duped", "tricked", "attacked", "killed", "violated"
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
	"joy": [
		"you seem pleased with yourself",
		"what's so funny?",
		"what are you smiling about?",
		"are you happy because of me?"
	],
	"sorrow": [
		"what's the matter?",
		"what's wrong?",
		"are you feeling ok?",
		"you seem sad"
	],
	"anger": [
		"wow, calm down!",
		"geez, what got you so riled up?",
		"did i say something wrong?",
		"have i upset you?",
		"are you mad?"
	],
	"surprise": [
		"surprised?",
		"what's so shocking?",
		"didn't expect that?"
	],
	"headwear": [
		"nice hat",
		"cool hat",
		"i like your hat"
	],
	"join": [
		"hello there!",
		"and who might you be?",
		"are you friendly?"
	],
	"leave": [
		"leaving me already?",
		"where are you going?",
		"come back!"
	],
	"good": [
		"that rocks.",
		"that's what's up.",
		"heck yeah!",
		"awesome."
	],
	"bad": [
		"that sucks.",
		"laaaaaaaaaame.",
		"that's wack.",
		"that's rough.",
		"pretty evil, right?",
		"yikes.",
		"gross."
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
	"redirect": [
		"i wanna hear more about",
		"let's get back to",
		"wouldn't you rather talk more about",
		"i'd rather discuss"
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
		"ummm..",
		"you ask a lot of questions"
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