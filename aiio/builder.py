import os
from cantools.util import read, write, log, batch
from .think import identify, add_opinions
from model import Opinion

UNBRAK = False
FILTER = True
fcz = ["^", "*", "®"]

def blocks2sentences(blocks):
	ops = []
	for block in blocks:
		sentences = block.split(". ")
		for sentence in sentences:
			sent = sentence.replace("\n", " ").replace("  ", " ").replace("_", "").strip()
			if sent.startswith("[") or len(sent) < 25:
				continue
			if UNBRAK:
				while "[" in sent:
					s = sent.find("[")
					e = sent.find("]", s)
					sent = sent[:s] + sent[e+1:]
			ops.append(sent)
	return ops

def opinionate(data):
	if FILTER:
		for fc in fcz:
			data = data.replace(fc, "")
	blocks = data.split("\n\n")
	blen = len(blocks)
	ops = []
	progress = 0
	def sentencer(bset):
		nonlocal progress
		progress += len(bset)
		ops.extend(blocks2sentences(bset))
		log("processed %s of %s blocks"%(progress, blen))
		log("compiled %s opinions"%(len(ops),))
	log("processing %s blocks"%(blen,), important=True)
	batch(blocks, sentencer, chunk=100)
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