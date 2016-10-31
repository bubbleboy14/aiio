import random
from model import *
from think import learn, phrase, meaning, question, identify, tag, nextNoun, retorts
from util import randphrase
from hear import listen
from speak import say, setBrevity
"""
[('who', 'WP'), ('are', 'VBP'), ('you', 'PRP'), ('?', '.')]
[('who', 'WP'), ('is', 'VBZ'), ('john', 'NN'), ('?', '.')]
[('who', 'WP'), ('eats', 'VBZ'), ('cheerios', 'NNS'), ('?', '.')]
[('who', 'WP'), ('am', 'VBP'), ('i', 'RB'), ('?', '.')]
[('i', 'NN'), ('am', 'VBP'), ('mario', 'NN')]
"""

MOODS = {
	"all": ["inquire", "rephrase", "support", "refute"],
	"happy": ["support"],
	"grumpy": ["refute"],
	"inquisitive": ["inquire", "rephrase"]
}

class Brain(object):
	def __init__(self, name, mood="all", ear=False, retorts=True, fallback=False, brief=True):
		self.name = name
		self._identity = identify(name).key
		self._examiner = None
		self.mood = mood == "random" and random.choice(MOODS.keys()) or mood
		self.retorts = retorts
		self.fallback = fallback
		setBrevity(brief)
		if ear:
			self.ear = listen(self)

	def __call__(self, sentence):
		sentence = sentence.lower()
		tagged = tag(sentence)
		if tagged[0][1] in ["WP", "WRB"]:
			return say(self.answer(sentence))
		elif sentence.startswith("tell me"):
			subject = sentence.split(" about ")[1]
			return say(self.pinfo(subject=subject))
		else:
			return say(self.ingest(sentence) or (self.retorts and self.retort(sentence)) or (self.fallback and randphrase("unsure")))

	def pinfo(self, person=None, subject=None):
		if not person:
			if "you" in subject:
				person = self.identity()
			elif subject == "me":
				person = self.examiner()
				if not person:
					return randphrase("exhausted",
						"you don't know yourself?")
			else:
				person = identify(subject)
		content = person.content()
		if content == person.name and subject:
			content = learn(subject, True).meaning()
		if content:
			return content
		else:
			return randphrase("exhausted")

	def identity(self):
		return self._identity.get()

	def examiner(self, name=None):
		if not self._examiner and name:
			self._examiner = identify(name).key
		return self._examiner and self._examiner.get()

	def ingest(self, sentence):
		# glean information, populate topics{} and history[]
		tagged = tag(sentence)
		if len(tagged) > 1:
			if tagged[0][0] == "i" and tagged[1][0] == "am":
				desc = sentence[5:]
				examiner = self.examiner(nextNoun(tagged[2:]))
				if not examiner.summary:
					examiner.summary = desc
				else:
					examiner.description = "%s %s"%(examiner.description, desc)
				examiner.qualifiers.append(phrase(desc).key)
				examiner.put()
				q = question("who am i?")
				q.answers.append(examiner.key)
				q.put()
				# what's going on here? no qualifiers???
				if examiner.qualifiers: # should ALWAYS be qualifiers :-\
					qual = random.choice(examiner.qualifiers).get().content()
					qper = []
					for (qword, qpos) in tag(qual):
						if qpos == "PRP" and qword in ["i", "me"]:
							qword = "you"
						elif qpos == "PRP$" and qword == "my":
							qword = "your"
						qper.append(qword)
					return " ".join(qper)
				return "%s %s"%(randphrase("greeting"), examiner.name)
			elif "because" in sentence:
				event, reason = sentence.split(" because ")
				Reason(person=self._examiner, name=event, reason=phrase(reason)).put()
				return "%s %s because %s?"%(randphrase("rephrase"),
					event, reason)
			elif tagged[0][1].startswith("NN"):
				if tagged[1][0] in ["is", "are"]: # learn it!
					mdef = " ".join([w for (w, p) in tagged[2:]])
					meaning(tagged[0][0], mdef)
					return randphrase("noted")
				else:
					pass # handle other verbs!!

	def clarify(self, sentence):
		return randphrase("what")

	def answer(self, sentence):
		q = question(sentence)
		if not q.answers:
			tagged = tag(sentence)
			print tagged
			if tagged[0][0] == "who":
				if tagged[1][0] in ["is", "are"]:
					if tagged[2][0] == "you":
						q.answers.append(self._identity)
					else:
						q.answers.append(identify(nextNoun(tagged[2:])).key)
				elif tagged[1][0] == "am":
					person = self.examiner()
					if person:
						return self.pinfo(person=person)
					return randphrase("exhausted",
						"i don't know. who do you think you are?")
				else:
					return randphrase("what")
			elif tagged[0][0] == "what":
				if tagged[1][0] in ["is", "are"]:
					obj = learn(nextNoun(tagged[2:]), True)
					meanings = obj.meanings()
					if not meanings:
						return "%s. what does %s mean to you?"%(randphrase("unsure"), obj.word)
					q.answers.append(meanings[0].key)
				else:
					return randphrase("what")
			elif tagged[0][0] == "where":
				place = getPlace(nextNoun(tagged[2:]))
				location = place.getLocation()
				return location.name
			elif tagged[0][0] == "why":
				return randphrase("exhausted",
					"nevermind the whys and wherefores!") # placeholder
				# TODO: first check reason. then... something?
			else: # when/why: yahoo answers api?
				return randphrase("what")
			q.put()
		return random.choice(q.answers).get().content()

	def retort(self, sentence):
		retz = MOODS[self.mood]
		random.shuffle(retz)
		for r in retz:
			v = retorts[r](sentence)
			if v:
				v = v.replace(self.identity().name, "i")
				return self._examiner and v.replace(self.examiner().name, "you") or v

brains = {}

def getBrain(name=None, mood="all", ear=False, retorts=True, fallback=False):
	if name in brains:
		return brains[name]
	brains[name] = Brain(name, mood, ear, retorts, fallback)
	return brains[name]