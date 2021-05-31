import random, nltk
from . import speak, iverbs, util
from cantools import db, geo

POS = { "JJ": "adj", "VB": "v", "NN": "n" }
IRR = {
    "be": {
        "root": "be",
        "first": "am",
        "second": "are",
        "third": "is",
        "past": "was",
        "gerund": "being"
    },
    "have": {
        "root": "have",
        "first": "have",
        "second": "have",
        "third": "has",
        "past": "had",
        "gerund": "having"
    }
}
IRR["am"] = IRR["be"]
IRR["are"] = IRR["be"]
IRR["is"] = IRR["be"]
IRR["was"] = IRR["be"]
IRR["being"] = IRR["be"]
IRR["has"] = IRR["have"]
IRR["had"] = IRR["have"]
IRR["having"] = IRR["have"]
VMAP = {
    "VB": "first",
    "VBP": "second",
    "VBZ": "third",
    "VBD": "past",
    "VBN": "participle",
    "VBG": "gerund"
}
NEGS = {
    "first": "don't",
    "second": "don't",
    "third": "doesn't",
    "past": "didn't",
    "gerund": "not"
}
IPP = {}

for line in iverbs.IV.split("\n"):
    v, p, pp = line.split("\t")
    IPP[v] = IPP[p] = IPP[pp] = {
        "past": p,
        "participle": pp
    }

class Symbol(db.TimeStampedBase):
    def meanings(self, count=False):
        q = Meaning.query(Meaning.synonyms.contains(self.key.urlsafe()))
        if count:
            return q.count()
        return q.all()

    def meaning(self):
        q = Meaning.query(Meaning.synonyms.contains(self.key.urlsafe()))
        r = q.fetch(1, random.randint(0, q.count()))
        return r and r[0]

    def opposite(self):
        q = Meaning.query(Meaning.antonyms.contains(self.key.urlsafe()))
        r = q.fetch(1, random.randint(0, q.count()))
        return r and r[0]

def stem(word, hard=False):
    if word.endswith("ed"):
        word = word[:-2]
    if word.endswith("ing"):
        word = word[:-3]
    if hard and word.endswith("s"):
        word = word[:-1]
    return word

class Word(Symbol):
    word = db.String()

    def content(self):
        return self.word

    def negate(self, pos):
        if pos.startswith("VB"):
            if self.word in IRR:
                return "%s not"%(self.word,)
            return "%s %s"%(NEGS[VMAP[pos]], self.word)
        if pos.startswith("JJ"): # careful (sometimes 'i')
            return "not %s"%(self.word,)

    # functions below are for VERBS ONLY (self.meanings()[x].part == 'v')
    def root(self):
        w = IRR.get(self.word)
        return w and w["root"] or stem(self.word)

    def first(self):
        w = IRR.get(self.word)
        return w and w["first"] or self.root()

    def second(self):
        w = IRR.get(self.word)
        return w and w["second"] or self.root()

    def third(self):
        w = IRR.get(self.word)
        r = self.root()
        return w and w["third"] or r.endswith("s") and r or "%ss"%(r,)

    def gerund(self):
        w = IRR.get(self.word)
        r = self.root()
        return w and w["gerund"] or r.endswith("e") and "%sing"%(r[:-1],) or "%sing"%(r,)

    def past(self):
        # doesn't account for was/were :-\
        w = IRR.get(self.word) or IPP.get(self.word)
        r = self.root()
        return w and w["past"] or r.endswith("e") and "%sd"%(r,) or "%sed"%(r,)

    def participle(self):
        w = IPP.get(self.word)
        return w and w["participle"] or self.past()

    def conjugate(self, part):
        return getattr(self, VMAP[part])()

    def parts(self):
        return {
            "root": self.root(),
            "first": self.first(),
            "second": self.second(),
            "third": self.third(),
            "gerund": self.gerund(),
            "past": self.past()
        }

class Phrase(Symbol): # a complete thought - "you bet!"
    words = db.ForeignKey(kind=Word, repeated=True)
    phrase = db.String()

    def content(self):
        return self.phrase

class Idea(Symbol):
    expressions = db.ForeignKey(kinds=[Word, Phrase], repeated=True)

    def content(self):
        if not len(self.expressions):
            print("Idea.content(): no expressions!")
        return self.expressions[random.randint(0, len(self.expressions) - 1)].get().content()

class Meaning(db.TimeStampedBase):
    synonyms = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True)
    antonyms = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True)
    part = db.String(default="n") # v, n, adj, adv
    definition = db.Text()

    def content(self):
        if not self.definition:
            print("Meaning.content(): no definition!")
        return self.definition

class Object(Idea):
    name = db.String()
    qualifiers = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True) # adjectives mostly
    summary = db.String()
    description = db.Text()

    def content(self):
        return self.summary

class Place(Object): # where
    location = db.ForeignKey(kind="place")

    def getLocation(self):
        if not self.location:
            self.location = getPlace(geo.where(self.name)).key
            self.put()
        return self.location.get()

def getPlace(pname):
    place = Place.query(Place.name == pname).get()
    if not place:
        place = Place(name=pname)
        place.put()
    return place

class Event(Object): # when
    location = db.ForeignKey(kind=Place)
    moment = db.DateTime()

class Person(Object): # who
    birth = db.ForeignKey(kind=Event)
    residence = db.ForeignKey(kind=Place)

    def content(self):
        return self.qualifiers and random.choice(self.qualifiers).get().content() or self.summary or self.description or self.name

    def opinion(self, topic): # topic already lowercase
        # do this better -- single query would be ideal
        oz = Opinion.query(Opinion.person == self.key).all()
        pk = Phrase.query(Phrase.key.in_([o.phrase for o in oz]),
            db.func.lower(Phrase.phrase).like("%%%s%%"%(topic,))).all()
        if pk:
            sents = nltk.sent_tokenize(random.choice(pk).phrase)
            for sent in sents:
                if topic in sent.lower():
                    return sent
        # split up!
        if " " in topic:
            tz = topic.split(" ")
            tz.sort(lambda a, b: len(a) < len(b) and 1 or -1)
            for part in tz:
                op = self.opinion(stem(part, True))
                if op:
                    return op

    # version 1 (current): use util words directly
    # version 2 (future) : check synonyms/forms
    def _scan(self, words):
        sentences = nltk.sent_tokenize(self.description)
        hits = []
        for sentence in sentences:
            for word in words:
                if word in sentence:
                    hits.append(sentence)
        return hits

    def info(self):
        asps = {}
        for asp, words in util.aspects.items():
            asps[asp] = self._scan(words)
        return asps

    def assessment(self):
        for pers, words in util.personalities:
            hits = self._scan(words)
            if hits:
                return "%s. %s is a %s."%(speak.truncate(random.choice(hits)),
                    self.name, pers)

class Thing(Object): # what
    purpose = db.ForeignKey(kind=Idea)

class Action(Object):
    verbs = db.ForeignKey(kinds=[Word, Phrase])

class Emotion(Idea):
    emotion = db.ForeignKey(kind=Word)

class Reason(Object): # why
    person = db.ForeignKey(kind=Person)
    reason = db.ForeignKey(kind=Phrase)

    def content(self):
        if self.person:
            return "%s says %s because %s"%(self.person.name, self.name, self.reason.content())
        return "%s because %s"%(self.name, self.reason.content())

class Method(Action): # how
    action = db.ForeignKey(kind=Action)
    rationale = db.ForeignKey(kind=Reason)

class Strategy(Object): # why
    methods = db.ForeignKey(kind=Method, repeated=True)

class Affinity(db.TimeStampedBase):
    person = db.ForeignKey(kind=Person)
    idea = db.ForeignKey(kind=Idea)
    value = db.Float() # -1.0 to 1.0

class Opinion(db.TimeStampedBase):
    person = db.ForeignKey(kind=Person)
    phrase = db.ForeignKey(kind=Phrase)

class Question(db.TimeStampedBase):
    phrase = db.ForeignKey(kind=Phrase) # who what when where why how
    answers = db.ForeignKey(kinds=[Word, Phrase, Idea, Meaning, Object, Person], repeated=True)