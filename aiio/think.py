import random, nltk, duckduckgo_search, wikipedia
try: # py2
	from commands import getoutput
except: # py3
	from subprocess import getoutput
from cantools.web import fetch, strip_html
from cantools.util import log, error, batch
from . import speak
from model import *
from .util import randphrase, values

def load_corpora():
	for item in ["maxent_ne_chunker", "words", "averaged_perceptron_tagger", "punkt"]:
		nltk.download(item)

load_corpora()
ddgs = DDGS()

_padding = "\n\n  %s\n      "

def learn(word, deep=False):
	w = Word.query(Word.word == word).get()
	if not w:
		log("learning %s"%(word,))
		w = Word(word=word)
		w.put() # for recursion...
	puts = []
	if deep and not w.meanings(True):
		o = getoutput('dict -d wn "%s"'%(word,))
		if not o.startswith("No"):
			options = [word, word.lower(), word.title()]
			for option in options:
				padded = _padding%(option,)
				if padded in o:
					o = o.split(padded)[1]
					break
			dz = o.replace("\n%s"%(" " * 13,), " ").replace("\n%s"%(" " * 11,),
				" ").replace("\n%s"%(" " * 9,), " ").split("\n      ")
			for d in dz:
				if not d[0].isdigit(): # new part
					part, d = d.split(" ", 1)
				m = Meaning(part=part)
				d = d.split(": ", 1)[1]
				if " [ant: {" in d:
					d, aline = d.split(" [ant: {")
					antz = aline[:-2].split("}, {")
					m.antonyms = [wordorphrase(aword).key for aword in antz]
				if " [syn: {" in d:
					d, sline = d.split(" [syn: {")
					synz = sline[:-2].split("}, {")
					m.synonyms = [wordorphrase(sword).key for sword in synz]
				m.definition = d
				puts.append(m)
		if not w.meanings(True):
			puts.append(Meaning(definition=summy(w.word), synonyms=[w.key]))
	puts and db.put_multi(puts)
	return w

def phrase(p):
	pent = Phrase.query(Phrase.phrase == p).get()
	if not pent:
		stripped = [c for c in p if c.isalpha() or c.isspace()]
		pent = Phrase(phrase=p, words=[learn(w).key for w in "".join(stripped).split(" ")])
		pent.put()
	return pent

def wordorphrase(s):
	return " " in s and phrase(s) or learn(s)

def facts(subject): # people only so far!!
	person = identify(subject)
	return {
		"info": person.info(),
		"assessment": person.assessment()
	}

def assess(subject, identity=None):
	if identity:
		# check for opinions
		# 1) full phrase
		# 2) by word
		op = identity.opinion(subject)
		if op:
			return op
	person = identify(subject)
	az = person.assessment()
	if az:
		return az
	info = person.info()
	cresp = evaluate(info["creations"])
	if cresp:
		return cresp
	for aspect in ["opinions", "attractions", "aversions"]:
		if info[aspect]:
			return random.choice(info[aspect])
	return evaluate(person.description.split(". "))

def evaluate(phrases):
	for phrase in phrases:
		for value, words in values.items():
			for word in words:
				if word in phrase:
					return "%s - %s"%(speak.truncate(phrase), randphrase(value))

def meaning(q, a):
	m = Meaning(synonyms=[wordorphrase(q).key], definition=a)
	m.put()
	return m

def question(q):
	p = phrase(q)
	return Question.query(Question.phrase == p.key).get() or Question(phrase=p.key)

def wsum(name):
	print("checking wikipedia for", name)
	try:
		return wikipedia.summary(name).replace("\n", " ")
	except wikipedia.DisambiguationError as e:
		try:
			return wikipedia.summary(str(e).split("\n")[1])
		except wikipedia.DisambiguationError as e:
			return "" # right? would be nice to indicate the term is too ambiguous...
	except Exception:
		return ""

def dsum(name):
	print("checking duckduckgo for", name)
	res = ddgs.text(name, max_results=1)
	return res and res[0]['body']

def summy(name):
	return dsum(name) or wsum(name)
#	return ("%s %s"%(dsum(name), wsum(name))).strip()

def research(entity):
	summary = summy(entity.name)
	if summary:
		entity.description = summary
		entity.summary = speak.truncate(summary)
		entity.qualifiers = [phrase(p.strip()).key for p in entity.summary.split(". ")]
	else:
		print("thing.research() FAILED for", entity)

def add_opinions(person, lines):
	numlines = len(lines)
	progress = 0
	def addops(ops):
		nonlocal progress
		progress += len(ops)
		person.add_opinions(ops)
		print("imported", progress, "of", numlines, "opinions")
	print("adding", numlines, "opinions")
	batch(lines, addops)

def find_opinions(person):
	res = fetch("en.wikiquote.org",
		"/w/api.php?format=json&action=parse&page=%s&prop=text"%("_".join(person.name.split(" ")),),
		protocol="https", asjson=True)
	if res and 'parse' in res:
		draw = strip_html(res['parse']['text']['*'])
		dlines = list(filter(lambda x: len(x) > 30,
			[d.split("\n\n")[0] for d in draw.split("\n\n\n\n\n")]))
		add_opinions(person, dlines)

def identify(name):
	print("identify", name)
	person = Person.query(Person.name == name).get()
	if not person:
		person = Person(name=name)
		research(person)
		person.put()
	return person

def tag(sentence):
	return nltk.pos_tag(nltk.word_tokenize(sentence.replace("can't", "can not").replace("n't", " not")))

def verbs(tagged):
	vz = []
	for t in tagged:
		if t[1].startswith("VB"):
			vz.append(t)
	return vz

def nextNoun(tagged, force=True, pros=False):
	noun = []
	lastPart = None
	for t in tagged:
		if t[1].startswith("NN") or t[1] == "JJ" or (pros and t[1] == "PRP"):
			noun.append(t[0])
			lastPart = t[1]
		elif noun:
			break
	if force and not noun:
		for t in tagged:
			if noun and t[1] == ".":
				break
			else:
				noun.append(t[0])
	if len(noun) > 1 and lastPart == "JJ":
		noun.pop()
	return " ".join(noun)

def inquire(sentence, mood=None): # only return if word is unknown or mood{}
	for (word, pos) in tag(sentence):
		deep = len(word) > 3
		w = learn(word, deep)
		if deep and not w.meanings(True):
			return "%s %s"%(randphrase("inquire"), word)
	if mood:
		susp = mood["suspicion"] > mood["curiosity"]
		if susp:
			head = "challenge"
			tail = mood["ego"] + mood["mad"] > mood["happy"] and "accuse" or "doubt"
		else:
			head = "wonder"
			tail = "muse"
		return "%s ... %s"%(rephrase(sentence, head), randphrase(tail))

# also support identity assignment ("I" instead of "Joe Whatever")
def _invert(sentence): # reverse/retag 1st/2nd person
	orig = tag(sentence)
	log("orig: %s"%(orig,))
	tagged = []
	lastword = None
	lastpart = None
	for (word, part) in orig:
		if part == "VB" or part == "VBP":
			part = part == "VBP" and "VB" or "VBP"
			if word == "am":
				word = "are"
			elif word == "are":
				word = "am"
			else:
				word = learn(word).conjugate(part)
		elif word == "i":
			word = "you"
		elif word == "my":
			word = "your"
		elif word == "your":
			word = "my"
		elif word == "mine":
			word = "yours"
		elif word == "yours":
			word = "mine"
		elif part == "NN" and word == "you":
			word = "i"
		elif part == "PRP":
			if word == "me":
				word = "you"
			elif word == "you":
				word = (lastpart == "IN" and lastword not in ["that", "than"]) and "me" or "i"
		lastword = word
		lastpart = part
		tagged.append((word, part))
	log("tagged: %s"%(tagged,))
	return tagged

def invert(sentence):
	return " ".join([a for (a, b) in _invert(sentence)])

def _getalt(word, tpos, opposite=False):
	vmeanz = [m for m in learn(word, len(word) > 3).meanings() if m.part == POS.get(tpos)]
	if vmeanz:
		random.shuffle(vmeanz)
		for mng in vmeanz:
			altz = None
			if opposite and mng.antonyms:
				altz = [a for a in db.get_multi(mng.antonyms) if a.modeltype() == "word" and a.word != word]
			elif not opposite and mng.synonyms:
				altz = [s for s in db.get_multi(mng.synonyms) if s.modeltype() == "word" and s.word != word]
			if altz:
				alt = random.choice(altz)
				log("swapped '%s' for '%s'"%(alt.content(), word))
				return alt.content()

def _rephrase(sentence, tpos, opposite=False):
	# tokenize, replace words w/ synonyms/antonyms
	swapped = False
	new = []
	for (word, pos) in tag(sentence):
		if pos.startswith(tpos):
			new.append(_getalt(word, tpos, opposite) or word)
		else:
			new.append(word)
	return " ".join(new)

def restate(sentence, force=False):
	s = _rephrase(_rephrase(_rephrase(_rephrase(sentence, "VB"), "NN"), "JJ"), "VBG")
	if force and s == sentence:
		return random.choice([
			"%s %s"%(randphrase("just saying"), s),
			"%s - %s"%(s, randphrase("how else")),
			randphrase("no repeat")
		])
	return s

def rephrase(sentence, preface="rephrase", mood=None):
	resp = "%s %s"%(randphrase(preface), invert(restate(sentence)))
	if mood and mood["vibe"] != "all":
		resp = "%s ... %s"%(resp, randphrase(mood["vibe"]))
	return resp

def support(sentence, mood=None):
	# tokenize, replace adjective/verb w/ synonym
	resp = "%s %s"%(randphrase("agree"), invert(_rephrase(_rephrase(sentence, "JJ"), "VB")))
	if mood:
		resp = "%s ... %s"%(resp,
			randphrase(mood["ego"] > mood["happy"] and "boast" or "compliment"))
	return resp

def query2statement(query, tagged=None):
	tagged = tagged or tag(query)
	noun = nextNoun(tagged, pros=True)
	return invert("%s %s"%(noun, query[4:].replace(" %s"%(noun,), "")))

def tellmewhy(query, tagged=None):
	statement = query2statement(query, tagged)
	return Reason.query(Reason.name == statement).all()

negz = {
	" no ": "",
	" not ": "",
	" isn't ": " is ",
	" aren't ": " are ",
	" weren't ": " were ",
	" don't ": " do ",
	" doesn't ": " does ",
	" can't ": " can ",
	" won't ": " will "
}
posz = {
	" is ": " isn't ",
	" are ": " aren't ",
	" were ": " weren't ",
	" do ": " don't ",
	" does ": " doesn't ",
	" can ": " can't ",
	" will ": " won't "
}

def negate(sentence):
	for neg in negz:
		if neg in sentence:
			log("negating on %s"%(neg,))
			return sentence.replace(neg, negz[neg])
	for pos in posz:
		if pos in sentence:
			log("negating on %s"%(pos,))
			return sentence.replace(pos, posz[pos])
	negated = False
	words = []
	for (word, pos) in tag(sentence):
		if not negated and pos.startswith("VB"):
			log("negating %s"%(word,))
			word = learn(word).negate(pos)
			log("with %s"%(word,))
			negated = True
		words.append(word)
	return " ".join(words)

def refute(sentence, mood=None):
	# tokenize, replace adjective w/ antonym, noun w/ synonym
	negation = _rephrase(sentence, "JJ", True)
	if negation == sentence:
		negation = negate(sentence)
	resp = "%s %s"%(randphrase("disagree"), invert(_rephrase(negation, "NN")))
	if mood:
		if mood["mad"] > mood["sad"]:
			if mood["mad"] > 0.8:
				tail = "insult"
			else:
				tail = "chastise"
		elif mood["sad"] > 0.8:
			tail = "lament"
		else:
			tail = "doubt"
		resp = "%s ... %s"%(resp, randphrase(tail))
	return resp

retorts = {
	"inquire": inquire,
	"rephrase": rephrase,
	"support": support,
	"refute": refute
}