import random
from .raw.quotes import quotes as raw_quotes

class Quoter(object):
	def __init__(self):
		self.authors = {}
		self.tags = {}
		self.load()

	def quote(self, topic=None, author=None):
		options = []
		tier2 = []
		if author:
			if author in self.authors:
				for quote in self.authors[author]:
					tier2.append(quote)
					if quote['tag'] in topic or topic in quote['text']:
						options.append(quote)
		if topic:
			for tag in self.tags:
				if tag in topic:
					for quote in self.tags[tag]:
						tier2.append(quote)
						if topic in quote['text']:
							options.append(quote)
		options = options or tier2
		if options:
			return random.choice(options)

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