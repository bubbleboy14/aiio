import random

triggers = {
	"opinion": [
		"what do you think of",
		"what do you think about",
		"what do you know about",
		"what can you tell me about",
		"what are your thoughts on",
		"what's your take on",
		"how do you feel about",
		"what's your opinion of",
		"have you heard about",
		"have you heard of",
		"what about",
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
		"murdered", "invaded", "terrorized", "tortured", "abused", "enslaved", "raped"
	]],
	["psycho", [
		"killed", "kidnapped", "abducted", "groomed", "procured", "molested", "maimed"
	]],
	["villain", [
		"attacked", "harassed", "violated", "cheated", "perjured", "oppressed"
	]],
	["scammer", [
		"misled", "duped", "tricked", "defrauded", "embezzled", "stole", "lied"
	]],
	["hero", [
		"saved", "rescued", "liberated", "freed", "emancipated", "rebuilt"
	]],
	["genius", [
		"invented", "discovered", "developed", "pioneered", "revolutionized", "patented"
	]],
	["jerk", [
		"hurt", "harmed", "injured", "damaged", "ruined"
	]],
	["homie", [
		"helped", "supported", "assisted", "restored", "beautified", "revitalized", "donated"
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
		"love the hat",
		"groovy headwear",
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
		"sounds good to me!",
		"that's fantastic!"
	],
	"bad": [
		"how sad.",
		"it's appalling.",
		"that sucks.",
		"how awful.",
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
		"it sounds like you're saying that",
		"you're basically saying that"
	],
	"inquire": [
		"please elaborate on",
		"tell me more regarding",
		"what do you know about",
		"what can you tell me about",
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
	"next": [
		"what else is new?",
		"how have you been?",
		"how are things besides that?"
	],
	"unsure": [
		"i'm not sure",
		"it's hard to say",
		"ummm..",
		"i don't have all the answers",
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
		"i don't care dude, do you?",
		"i guess i just don't know",
		"dude, i could care less"
	],
	"claims": [
		"claims", "claimed", "says", "said", "once said", "famously asserted",
		"believes", "believed", "thinks", "thought", "was sure",
		"has stated", "wants us to think", "seems sure that"
	],
	"anonymous": [
		"an unknown person", "someone wise", "someone thoughtful",
		"an old friend", "a little bird i know", "an anonymous author"
	],
	"boast": [
		"i knew you'd come around!",
		"i'm happy you agree!",
		"so glad you see it my way",
		"right again!",
		"take it from me, kid!",
		"now you're getting it!"
	],
	"compliment": [
		"that's exactly right!",
		"you hit the nail on the head!",
		"very impressive!",
		"you're quite charming!",
		"i'm so proud of you!",
		"you're making a lot of sense!",
		"that's quite clever!",
		"i knew we'd get along!"
	],
	"insult": [
		"you're a kook",
		"how stupid are you?",
		"you make me sick",
		"you're disgusting",
		"you idiot!",
		"you should be ashamed"
	],
	"chastise": [
		"why would you say something like that?",
		"what's wrong with you?",
		"how could you think that?",
		"you're embarrassing yourself"
	],
	"doubt": [
		"are you sure?",
		"that can't be right",
		"i don't think that's the case",
		"i doubt it",
		"i highly doubt it",
		"that couldn't possibly be true",
		"i don't think so",
		"i don't believe you",
		"i refuse to believe it",
		"you don't know what you're talking about",
		"why should i believe you?",
		"that doesn't pass the sniff test",
		"doesn't add up",
		"that doesn't seem credible",
		"where did you hear that?",
		"sounds like fake news",
		"yeah right!",
		"poppycock!",
		"what a pile of rubbish!",
		"sounds very unlikely!",
		"hah, that's rich!",
		"a likely story!",
		"that's preposterous",
		"did you hear that from alex jones?",
		"sure, and i'm the queen of england!"
	],
	"lament": [
		"no one gets me",
		"it's like i'm talking to a wall",
		"another sad conversation",
		"you must think i'm crazy",
		"you probably hate me",
		"why doesn't anyone understand me?"
	],
	"muse": [
		"is that possible?",
		"how intriguing!",
		"i wonder...",
		"what a strange mystery...",
		"so many possibilities!"
	],
	"wonder": [
		"could it be that",
		"is it possible that",
		"i wonder if",
		"so you think that",
		"are you saying that"
	],
	"challenge": [
		"there's no way that",
		"i can't believe that",
		"you're wrong to say that"
	],
	"accuse": [
		"that's a laugh coming from you!",
		"look in the mirror, you jerk!",
		"i blame you"
	],
	"happy": [
		"it's such a pleasure talking to you!",
		"you're a delight!",
		"life is beautiful",
		"what a lovely day!"
	],
	"grumpy": [
		"this is boring",
		"i can't bring myself to care",
		"do i look like i care?",
		"whatever, sure",
		"fine, if you say so"
	],
	"inquisitive": [
		"the world is wide and weird!",
		"i have so many questions",
		"that really gets me thinking",
		"makes ya think, huh?",
		"interesting point!",
		"really makes ya wonder!",
		"is that all there is to it?",
		"i can't help but wonder if there's more to it..."
	]
}

def randphrase(ptype, extra=None):
	if extra:
		return random.choice(phrases[ptype] + [extra])
	return random.choice(phrases[ptype])