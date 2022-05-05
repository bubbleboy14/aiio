import os
from cantools.util import read, write, log
from .think import identify, add_opinions
from model import Opinion

def opinionate(data):
	ops = []
	blocks = data.split("\n\n")
	for block in blocks:
		sentences = block.split(". ")
		for sentence in sentences:
			sent = sentence.replace("\n", " ").replace("  ", " ").replace("_", "").strip()
			if sent.startswith("[") or len(sent) < 25:
				continue
			while "[" in sent:
				s = sent.find("[")
				e = sent.find("]", s)
				sent = sent[:s] + sent[e+1:]
			ops.append(sent)
	log("uniquifying %s statements"%(len(ops),), 1)
	ops = list(set(ops))
	log("derived %s opinions"%(len(ops),), 1)
	return ops

def brainify(name, data):
	person = identify(name)
	oz = Opinion.query(Opinion.person == person.key).all()
	if oz:
		return log("%s has %s opinions - skipping!"%(name, len(oz)))
	add_opinions(person, opinionate(data))

def brains():
	bz = os.listdir("brains")
	for b in bz:
		brainify(b[:-4], read(os.path.join("brains", b)))