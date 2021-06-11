import random, string
from model import *
from .think import learn, phrase, meaning, question, identify, find_opinions, tag, nextNoun, retorts, assess
from .util import triggers, randphrase
from .hear import listen
from .speak import say, setBrevity
from .quoter import Quoter
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
		self.opinionate()
		self._examiner = None
		self.mood = mood == "random" and random.choice(MOODS.keys()) or mood
		self.retorts = retorts
		self.fallback = fallback
		self.topics = []
		self.quoter = Quoter()
		setBrevity(brief)
		if ear:
			self.ear = listen(self)

	def __call__(self, sentence):
		if sentence.startswith("*"):
			return say(randphrase(sentence[1:]))
		sentence = sentence.lower()
		tagged = tag(sentence)
		quote = self.quote(sentence)
		if quote:
			return say(quote)
		opinion = self.opinion(sentence)
		if opinion:
			return say(opinion)
		if tagged[0][1] in ["WP", "WRB"]:
			return say(self.answer(sentence))
		if sentence.startswith("tell me"):
			subject = sentence.split(" about ")[1]
			return say(self.pinfo(subject=subject))
		return say(self.ingest(sentence) or (self.retorts and self.retort(sentence)) or (self.fallback and randphrase("unsure")))

	def quote(self, topic=None, author=None):
		q = self.quoter.respond(topic, (author or self.name).title())
		if q:
			print(q['author'], q['tag'], q['text'])
			if q['author'] == self.name:
				return q['text']
			else:
				a = q['author']
				if a == 'Anonymous':
					a = randphrase("anonymous")
				return "%s %s %s"%(a, randphrase("claims"), q['text'])

	def opinion(self, sentence):
		for trigger in triggers["opinion"]:
			if sentence.startswith(trigger):
				subject = sentence[len(trigger) + 1:].strip(string.punctuation)
				assessment = assess(subject, self.identity())
				if assessment:
					self.topics.append(subject)
					return assessment
				if self.topics:
					random.shuffle(self.topics)
					return "%s. %s %s..."%(randphrase("ambivalent"),
						randphrase("redirect"), self.topics.pop())
				sub = Person.query(Person.name == subject).get()
				if sub:
					return self.identity().assessment(sub) or self.meh(sub)
				sub = Word.query(Word.word == subject).get() or Phrase.query(Phrase.phrase == subject).get()
				if sub:
					return self.meh(sub.meaning().content())

	def meh(self, subject):
		return "%s - %s"%(subject.content(), randphrase("ambivalent"))

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
		return content or randphrase("exhausted")

	def identity(self):
		return self._identity.get()

	def opinionate(self):
		if not Opinion.query(Opinion.person == self._identity).count():
			find_opinions(self.identity())

	def examiner(self, name=None):
		if not self._examiner and name:
			self._examiner = identify(name).key
		return self._examiner and self._examiner.get()

	def ingest(self, sentence):
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
					return "%s ... %s"%(self._retort(sentence, "rephrase"), randphrase("noted"))
#					return randphrase("noted")
				else:
					pass # handle other verbs!!

	def clarify(self, sentence):
		return randphrase("what")

	def answer(self, sentence):
		q = question(sentence)
		if not q.answers:
			tagged = tag(sentence)
			print(tagged)
			if tagged[0][0] == "who":
				if tagged[1][0] in ["is", "are"]:
					if tagged[2][0] == "you":
						return "i'm %s"%(self.identity().name,)
					else:
						q.answers.append(identify(nextNoun(tagged[2:])).key)
				elif tagged[1][0] == "am":
					if "i talking to" in sentence:
						return "my name is %s"%(self.identity().name,)
					person = self.examiner()
					if person:
						return self.pinfo(person=person)
					return randphrase("exhausted",
						"i don't know. who do you think you are?")
				else:
					return randphrase("what")
			elif tagged[0][0] == "what":
				if tagged[1][0] in ["is", "are"]:
					if "your name" in sentence:
						return self.identity().name
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

	def _retort(self, sentence, responder):
		v = retorts[responder](sentence)
		if v:
			v = v.replace(self.identity().name, "i")
			return self._examiner and v.replace(self.examiner().name, "you") or v

	def retort(self, sentence):
		retz = MOODS[self.mood]
		random.shuffle(retz)
		for r in retz:
			v = self._retort(sentence, r)
			if v:
				return v

brains = {}

def getBrain(name=None, mood="all", ear=False, retorts=True, fallback=False):
	if name in brains:
		return brains[name]
	brains[name] = Brain(name, mood, ear, retorts, fallback)
	return brains[name]