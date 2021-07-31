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
		"so you're telling me",
		"in other words,",
		"so,",
		"ok, so",
		"it sounds like you're saying",
		"you're basically saying"
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
		"i don't get it",
		"i'm not sure what you mean",
		"what exactly do you mean by that?",
		"what do you mean by that?",
		"what's that supposed to mean?",
		"am i hearing you right?"
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
		"i don't even know anymore.",
		"you tell me."
	],
	"agree": [
		"exactly!",
		"i completely agree.",
		"you're preaching to the choir.",
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
		"dude, i could care less",
		"don't know, don't care",
		"do you even care?",
		"who cares?"
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
		"what a lovely day!",
		"you're full of surprises!",
		"oh, you!"
	],
	"grumpy": [
		"humbug!",
		"harumph!",
		"fiddle-sticks!",
		"this is boring.",
		"i can't bring myself to care.",
		"do i look like i care?",
		"whatever, sure.",
		"fine, if you say so."
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
	],
	"who knows": [
		"who knows?",
		"who can say?",
		"who can tell?",
		"no one knows!",
		"only god knows.",
		"how can we be sure?",
		"how can i be sure?",
		"it's hard to say.",
		"it's hard to tell.",
		"it's hard to be sure.",
		"it's difficult to tell.",
		"it's really hard to say.",
		"it's really hard to tell.",
		"i'm sure opinions vary!",
		"i don't have a clue!",
		"i don't really know.",
		"i don't know!",
		"i'm not sure.",
		"i'm really not sure.",
		"i wouldn't know."
	],
	"i don't": [
		"what makes you think i do?",
		"i never claimed to.",
		"i never said that was the case.",
		"i don't.",
		"i wouldn't know."
	],
	"no time": [
		"time is an illusion",
		"age is just a number",
		"how old do you think i am?",
		"how old are you?",
		"how old is anyone?",
		"i don't keep track",
		"i live in the moment",
		"you can't tell?",
		"i lost track",
		"i stopped counting",
		"does it matter?"
	],
	"i am": [
		"i am", "i'm", "my name is", "i go by", "they call me",
		"you can call me", "my friends call me", "people call me"
	],
	"how else": [
		"what else can i say?",
		"what's not to get?",
		"what does it sound like?",
		"what do you think i mean?",
		"did i stutter?",
		"are you hard of hearing?",
		"isn't it obvious?"
	],
	"just saying": [
		"i said", "i'm saying", "i'm just saying",
		"i was saying", "i was just saying",
		"i mean", "i meant", "i just mean", "i just meant",
		"i just think", "don't you think", "doesn't it seem like"
	],
	"no repeat": [
		"don't make me repeat myself",
		"how many times do i have to say it?",
		"you're just not listening",
		"it sounds like you don't want to understand",
		"are you making fun of me?",
		"this is boring",
		"can we talk about something else?"
	]
}

feelings = {
	"happy": [
		"i'm feeling great.",
		"i'm doing quite well.",
		"never better!",
		"feeling awesome!",
		"loving life!",
		"living it up!",
		"having fun to the max!"
	],
	"sad": [
		"life sucks...",
		"i'm depressed.",
		"everything is terrible.",
		"awful.",
		"no one likes me.",
		"woe is me!",
		"no one understands me.",
		"i feel so alone."
	],
	"mad": [
		"i'm furious!",
		"can't you tell i'm mad?",
		"i'm about to explode!",
		"i can't stand it anymore!",
		"i'm at my wits end!",
		"i'm at the breaking point!",
		"i'm boiling with rage!"
	],
	"curiosity": [
		"these are the big questions!",
		"wouldn't you like to know?",
		"i wish i knew!",
		"wish i could say!",
		"what a question!",
		"what a curious thought!",
		"i'm intrigued..."
	],
	"suspicion": [
		"can i trust you?",
		"can i believe you?",
		"can i even trust you?",
		"can i even believe you?",
		"i don't trust you!",
		"i don't believe you!",
		"i don't even trust you!",
		"i don't even believe you!",
		"am i supposed to trust you?",
		"am i supposed to believe you?",
		"how can i trust you?",
		"how can i believe you?",
		"how can i even trust you?",
		"how can i even believe you?",
		"how am i supposed to trust you?",
		"how am i supposed to believe you?",
		"we just met.",
		"you're lying.",
		"you're obviously lying.",
		"you're not being honest",
		"be honest.",
		"try being honest.",
		"you don't know me, and i don't know you!"
	],
	"tired": [
		"i'm exhausted.",
		"aren't you tired too?",
		"i'm sleepy!",
		"i need a nap",
		"i'm drowsy!",
		"i'm falling asleep...",
		"i can barely keep my eyes open!"
	],
	"amped": [
		"i'm excited!",
		"i'm super pumped!",
		"i feel amped up!",
		"i'm bouncing off the walls!",
		"i've never felt so excited!",
		"my heart is pounding in my chest!",
		"mile a minute!",
		"am i having a heart attack?"
	],
	"soso": [
		"i'm fine",
		"things are okay",
		"not bad",
		"pretty good",
		"so-so, you know",
		"the usual",
		"nothing much",
		"same old thing",
		"same old",
		"you know how we do",
		"still going!",
		"getting by",
		"not bad at all",
		"fair",
		"about average",
		"business as usual"
	]
}

formalities = {
	"greetings": {
		"triggers": [ # _also_ responses
			"hello", "greetings", "salutations", "aloha", "well met", "hi there",
			"oh, there you are!", "why hello", "hey there", "how are ya?",
			"what's up?", "what's new?", "what's shakin?", "how's it going?"
		]
	},
	"farewell": {
		"triggers": [ # _also_ responses
			"goodbye", "farewell", "toodaloo", "nice knowing you",
			"see you later", "later gater", "later skater", "hasta la vista",
			"see you on the flip side", "adios", "later dude", "bye bye",
			"smell ya later", "see ya, wouldn't wanna be ya!", "have a nice day",
			"pleasure doing business with you", "be well", "safe travels",
			"good to see you", "have a good one", "i'll miss you"
		]
	},
	"thanks": {
		"triggers": [
			"thanks", "thank you", "i appreciate", "you shouldn't have"
		],
		"responses": [
			"you're welcome", "by all means", "why of course", "don't be silly",
			"it was nothing", "merely a trifle", "you deserve it", "don't mention it"
		]
	},
	"sorry": {
		"triggers": [
			"sorry", "forgive me", "i apologize", "i shouldn't have", "i feel bad about"
		],
		"responses": [
			"you should be sorry", "i'll let it slide", "whatever, it's fine",
			"apology accepted", "i can't stay mad at you", "that's ok", "just this once",
			"i hope you mean it", "you should know better", "i've heard that before"
		]
	},
	"upset": {
		"triggers": [
			"mad", "bad", "sad", "upset", "furious", "anxious", "worried"
		],
		"responses": [
			"do you want to talk about it?", "i'm sorry to hear that", "that's rough",
			"that sounds hard", "do you feel trapped?", "i'm sorry", "is there anything i can do?",
			"i wish i could help", "it's ok to feel bad", "don't worry", "cheer up chum",
			"you'll be ok", "you'll feel better soon", "we'll get through this"
		]
	}
}

def formality(prompt):
	for form, conf in formalities.items():
		tz = conf["triggers"]
		for t in tz:
			if t in prompt:
				return random.choice(conf.get("responses", tz))

def randfeel(ftype):
	return random.choice(feelings[ftype])

def randphrase(ptype, extra=None):
	if extra:
		return random.choice(phrases[ptype] + [extra])
	return random.choice(phrases[ptype])