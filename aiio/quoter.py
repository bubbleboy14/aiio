import random
from .raw.quotes import quotes as raw_quotes

class Quoter(object):
	def __init__(self):
		self.authors = {}
		self.tags = {}
		self.cooldown = []
		self.load()

	def respond(self, topic, author=None):
		words = topic.split(" ")
		words.sort(key = lambda a : -len(a))
		resp = self.quote(topic, author, True)
		if resp:
			return resp
		for word in words:
			resp = self.quote(topic, author, True)
			if resp:
				return resp
		return self.quote(topic, author)

	def quote(self, topic=None, author=None, t1only=False):
		tier1 = []
		tier2 = []
		tier3 = []
		if author:
			if author in self.authors:
				for quote in self.authors[author]:
					tier2.append(quote)
					if quote['tag'] in topic or topic in quote['text']:
						tier1.append(quote)
		if topic and not t1only:
			for tag in self.tags:
				if tag in topic:
					for quote in self.tags[tag]:
						tier3.append(quote)
						if topic in quote['text']:
							tier2.append(quote)
		options = list(filter(lambda i : i not in self.cooldown, tier1 or tier2 or tier3))
		if options:
			sel = random.choice(options)
			if sel:
				self.cooldown.append(sel)
				self.cooldown = self.cooldown[-4:]
				return sel

	def load(self):
		for quote in raw_quotes:
			a = quote['author']
			if a not in self.authors:
				self.authors[a] = []
			self.authors[a].append(quote)
			t = quote['tag']
			if t not in self.tags:
				self.tags[t] = []
			self.tags[t].append(quote)