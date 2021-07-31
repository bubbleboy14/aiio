import random, string
from model import *
from .think import learn, phrase, meaning, question, identify, find_opinions, tag, nextNoun, retorts, assess, restate
from .util import triggers, randphrase, randfeel, formality
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

VIBES = {
    "all": ["inquire", "rephrase", "support", "refute"],
    "happy": ["support", "rephrase"],
    "grumpy": ["refute"],
    "inquisitive": ["inquire", "rephrase"]
}

"""
vu: mad, happy, sad, ego, suspicion, curiosity

happy : happy + ego
  ego : boast
  happy : compliment
grumpy : mad + sad
  mad : insult, chastise
  sad : doubt, lament
inquisitive : curiosity + suspicion
  curiosity : muse, wonder
  suspicion : challenge, doubt, accuse
"""

class Conversation(object):
    def __init__(self, name, partner):
        self.name = name
        self.partner = partner
        self.topics = []
        self.last = None

class Brain(object):
    def __init__(self, name, vibe="all", mood=None, options=None, ear=False):
        self.name = name
        self._identity = identify(name).key
        self.opinionate()
        self._examiner = None
        self.vibe = vibe == "random" and random.choice(VIBES.keys()) or vibe
        self.mood = mood
        mood and self.setMood(mood)
        self.options = {
            "quote": True,
            "opinion": True,
            "retort": True,
            "fallback": True,
            "brief": True
        }
        options and self.setOptions(options)
        self.quoter = Quoter()
        self.conversations = {}
        self.curconvo = None
        if ear:
            self.ear = listen(self)

    def _convo(self, name, partner):
        # multiple personalities w/ the same _identity_ may be distinguished by their individual _names_
        if name not in self.conversations:
            self.conversations[name] = {}
        if partner not in self.conversations[name]:
            self.conversations[name][partner] = Conversation(name, partner)
        return self.conversations[name][partner]

    def __call__(self, sentence, name=None, asker="rando"):
        name = name or self.name
        print("[INPUT]", sentence)
        self.curconvo = self._convo(name, asker)
        self.curconvo.last = resp = say(self._process(sentence))
        print("[OUTPUT]", resp)
        return resp

    def _process(self, sentence):
        if sentence.startswith("*"):
            return randphrase(sentence[1:])
        sentence = sentence.lower()
        if sentence.startswith("what do you mean"):
            return self.curconvo.last and restate(self.curconvo.last) or randphrase("who knows")
        if sentence.startswith("tell me") and " about " in sentence:
            return self.pinfo(subject=sentence.split(" about ")[1])
        resp = formality(sentence)
        if resp:
            return resp
        tagged = tag(sentence)
        if tagged[0][1] in ["WP", "WRB"]:
            return self.answer(sentence)
        return self.process(sentence) or self.ingest(sentence) or self.options["fallback"] and self.fallback()

    def setMood(self, mood, upvibe=True):
        self.mood = mood
        if not upvibe:
            return
        vecs = {
            "happy": mood["happy"] + mood["ego"] + 0.5,
            "grumpy": mood["mad"] + mood["sad"] + 1,
            "inquisitive": mood["curiosity"] + mood["suspicion"]
        }
        half = (vecs["happy"] + vecs["grumpy"] + vecs["inquisitive"]) / 2.0
        self.vibe = "all"
        for vec in vecs:
            if vecs[vec] >= half:
                self.vibe = vec
        self.mood["vibe"] = self.vibe
        print("setMood() - vibe:", self.vibe)

    def setOptions(self, options):
        for option in self.options: # enforce keyset
            if option in options:
                self.options[option] = options[option]
        setBrevity(self.options["brief"])

    def process(self, sentence):
        for option in ["quote", "opinion", "retort"]:
            if self.options[option]:
                print("checking", option)
                val = getattr(self, option)(sentence)
                if val:
                    return val

    def fallback(self, sentence=None):
        return "%s. %s"%(randphrase("unsure"), randphrase("next"))

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

    def _opinion(self, subject):
        assessment = assess(subject, self.identity())
        if assessment:
            self.curconvo.topics.append(subject)
            return assessment
        if self.curconvo.topics:
            random.shuffle(self.curconvo.topics)
            return "%s. %s %s..."%(randphrase("ambivalent"),
                randphrase("redirect"), self.curconvo.topics.pop())
        sub = Person.query(Person.name == subject).get()
        if sub:
            return self.identity().assessment(sub) or self.meh(sub)
        sub = Word.query(Word.word == subject).get() or Phrase.query(Phrase.phrase == subject).get()
        if sub:
            return self.meh(sub.meaning())

    def opinion(self, sentence):
        for trigger in triggers["opinion"]:
            if sentence.startswith(trigger):
                subject = sentence[len(trigger) + 1:].strip(string.punctuation)
                op = self._opinion(subject)
                if op:
                    return op

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
#                   return randphrase("noted")
                else:
                    pass # handle other verbs!!

    def clarify(self, sentence):
        base = "%s ... %s"%(self._retort(sentence, "rephrase"), randphrase("what"))
        if random.choice([True, False]):
            return "%s %s"%(self._feeling(), base)
        return base

    def answer(self, sentence):
        q = question(sentence)
        if not q.answers:
            tagged = tag(sentence)
            print(tagged)
            if tagged[0][0] == "who":
                if tagged[1][0] in ["is", "are"]:
                    if tagged[2][0] == "you":
                        return "%s %s"%(randphrase("i am"), self.curconvo.name)
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
                    return self.clarify(sentence)
            elif tagged[0][0] == "what":
                if tagged[1][0] in ["is", "are"]:
                    if "your name" in sentence:
                        return self.identity().name
                    obj = learn(nextNoun(tagged[2:]), True)
                    meanings = obj.meanings()
                    if not meanings:
                        return "%s. what does %s mean to you?"%(randphrase("unsure"), obj.word)
                    for meaning in meanings:
                        q.answers.append(meaning.key)
                else:
                    return self.clarify(sentence)
            elif tagged[0][0] == "where":
                place = getPlace(nextNoun(tagged[2:]))
                location = place.getLocation()
                return location.name
            elif tagged[0][0] == "why":
                return randphrase("exhausted",
                    "nevermind the whys and wherefores!") # placeholder
                # TODO: first check reason. then... something?
            elif tagged[0][0] == "how":
                if tagged[2][0] == "you":
                    if " about " in sentence:
                        op = self._opinion(sentence.split(" about ")[1])
                        if op:
                            return op
                    if len(tagged) > 3 and tagged[3][0] in ["know", "determine", "ensure", "believe"]:
                        return "%s %s"%(randphrase("i don't"), sentence[4:])
#                   if tagged[3][0] in ["feel", "feeling", "doing", "been"]:
                    return self._feeling()
                if tagged[1][0] == "old":
                    return randphrase("no time")
                return randphrase("who knows")
            else: # when/why: yahoo answers api?
                return self.clarify(sentence)
            q.put()
        return random.choice(q.answers).get().content()

    def _feeling(self):
        if self.vibe == "happy":
            return "%s %s"%(randfeel("happy"), randphrase("happy"))
        if self.vibe == "grumpy":
            grump = randphrase("grumpy")
            if self.mood:
                if self.mood["mad"] > self.mood["sad"]:
                    return "%s %s"%(grump, randfeel("mad"))
                else:
                    return "%s %s"%(grump, randfeel("sad"))
            return grump
        if self.vibe == "inquisitive":
            inq = randphrase("inquisitive")
            if self.mood:
                if self.mood["curiosity"] > self.mood["suspicion"]:
                    return "%s %s"%(randfeel("curiosity"), inq)
                else:
                    return "%s %s"%(randfeel("suspicion"), inq)
            return "%s %s"%(randphrase("who knows"), inq)
        if self.mood:
            if self.mood["energy"] > 0.6:
                return randfeel("amped")
            elif self.mood["energy"] < 0.4:
                return randfeel("tired")
        return randfeel("soso")

    def _retort(self, sentence, responder):
        v = retorts[responder](sentence, mood=self.mood)
        if v:
            v = v.replace(self.identity().name, "i")
            return self._examiner and v.replace(self.examiner().name, "you") or v

    def retort(self, sentence):
        retz = VIBES[self.vibe]
        random.shuffle(retz)
        for r in retz:
            v = self._retort(sentence, r)
            if v:
                return v

brains = {}

def getBrain(name=None, vibe="all", mood=None, options=None, ear=False):
    if name not in brains:
        brains[name] = Brain(name, vibe, mood, options, ear)
    else:
        if options:
            brains[name].setOptions(options)
        if mood:
            brains[name].setMood(mood)
        elif vibe:
            brains[name].vibe = vibe
    return brains[name]